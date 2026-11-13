"""
Step-up authentication with more than one worker process.

Two real Flask processes share one session directory, as with ``gunicorn -w 2``.
Each has its own in-memory cache, so these tests fail if a worker answers from
its cache instead of from the stored session. See ``testv2/step_up_worker.py``.
"""

import multiprocessing

import pytest

from testv2 import step_up_worker
from testv2.step_up_helpers import query

TIMEOUT = 20


@pytest.fixture(scope="module")
def workers(tmp_path_factory):
    session_dir = str(tmp_path_factory.mktemp("sessions"))
    context = multiprocessing.get_context("spawn")
    started = {}
    for name in ("A", "B"):
        parent, child = context.Pipe()
        process = context.Process(
            target=step_up_worker.run, args=(name, child, session_dir), daemon=True
        )
        process.start()
        started[name] = (process, parent)
    yield started
    for process, connection in started.values():
        try:
            connection.send(None)
        except OSError:
            pass
        process.join(5)
        if process.is_alive():
            process.terminate()


class Browser:
    """One browser session whose requests can land on either worker."""

    def __init__(self, workers):
        self._workers = workers
        self._cookie = None

    def get(self, worker, path):
        connection = self._workers[worker][1]
        connection.send((path, self._cookie))
        assert connection.poll(TIMEOUT), f"worker {worker} did not answer GET {path}"
        response = connection.recv()
        assert "error" not in response, response.get("error")
        self._cookie = response["cookie"]
        return response

    def callback(self, worker, code, started):
        """Deliver Kinde's callback for the request ``started`` to a worker."""
        state = query(started["location"])["state"]
        return self.get(worker, f"/callback?code={code}&state={state}")

    def sign_in(self, worker, code):
        return self.callback(worker, code, self.get(worker, "/login"))


@pytest.fixture
def browser(workers):
    return Browser(workers)


def test_a_session_is_visible_to_every_worker(browser):
    browser.sign_in("A", "login-shared")

    for worker in ("A", "B"):
        who = browser.get(worker, "/whoami")["json"]
        assert who["authenticated"] is True
        assert who["access_token"] == "access-login-shared"


def test_step_up_handled_by_another_worker_is_seen_everywhere(browser):
    browser.sign_in("A", "login-forward")
    assert browser.get("A", "/whoami")["json"]["acr"] is None  # cached on A

    started = browser.get("A", "/payouts")
    assert query(started["location"])["acr_values"] == "mfa"
    response = browser.callback("B", "stepup-forward", started)
    assert response["location"] == "http://localhost/payouts"

    # The worker that cached the single-factor tokens answers from the new ones
    who = browser.get("A", "/whoami")["json"]
    assert who["acr"] == "mfa"
    assert who["access_token"] == "access-stepup-forward"
    assert who["refresh_token"] == "refresh-from-stepup-forward"
    page = browser.get("A", "/payouts")
    assert page["status"] == 200 and page["body"] == "payouts"


def test_refresh_after_a_step_up_on_another_worker_uses_the_new_refresh_token(browser):
    browser.sign_in("A", "login-refresh")
    browser.get("A", "/whoami")
    browser.callback("B", "stepup-refresh", browser.get("A", "/payouts"))
    browser.get("A", "/whoami")

    browser.get("A", "/expire")
    refreshed = browser.get("A", "/whoami")

    assert refreshed["token_requests"] == [
        {
            "grant_type": "refresh_token",
            "code": None,
            "refresh_token": "refresh-from-stepup-refresh",
        }
    ]
    assert refreshed["json"]["acr"] == "mfa"
    assert refreshed["json"]["access_token"] == "access-refreshed-by-A"

    # The refreshed tokens were saved: the other worker uses them, without refreshing again
    other = browser.get("B", "/whoami")
    assert other["token_requests"] == []
    assert other["json"]["access_token"] == "access-refreshed-by-A"
    assert other["json"]["acr"] == "mfa"


def test_later_single_factor_sign_in_is_seen_by_a_worker_that_cached_mfa(browser):
    browser.sign_in("A", "login-reverse")
    browser.callback("A", "stepup-reverse", browser.get("A", "/payouts"))
    assert browser.get("A", "/payouts")["status"] == 200  # mfa, cached on A

    # A plain sign-in in the same browser session lands on the other worker
    browser.sign_in("B", "login-again")
    assert browser.get("B", "/whoami")["json"]["acr"] is None

    who = browser.get("A", "/whoami")["json"]
    assert who["acr"] is None
    assert who["access_token"] == "access-login-again"
    page = browser.get("A", "/payouts")
    assert page["status"] == 302
    assert query(page["location"])["acr_values"] == "mfa"
