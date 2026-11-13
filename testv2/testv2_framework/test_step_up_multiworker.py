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
