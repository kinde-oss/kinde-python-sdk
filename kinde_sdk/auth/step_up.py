"""
Step-up authentication (RFC 9470): the protocol logic shared by the OAuth clients.

Everything here is pure (no I/O, no framework access), so it can be reused by
framework integrations and by server-side checks on verified token claims.

Kinde's behaviour that this module encodes:

- ``acr_values`` is ``mfa`` or ``phr`` (phishing-resistant). ``phr`` also meets ``mfa``.
- Kinde omits the ``acr`` claim for a single-factor sign-in, so an absent
  ``acr`` means "neither ``mfa`` nor ``phr``".
- ``max_age`` is a non-negative whole number of seconds. ``0`` is valid. Kinde
  treats any other malformed value as "re-authenticate", which would hide a
  bug, so invalid values are rejected here before anything is sent.
"""

import re
import time
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Union


class AcrValues:
    """Authentication contexts that Kinde recognises in ``acr_values``."""

    MFA = "mfa"  # A second factor
    PHR = "phr"  # Phishing-resistant (a passkey with user verification); also meets MFA


AcrInput = Union[str, List[str], tuple]

# phr meets an mfa requirement; an absent acr ranks 0
_ACR_RANK = {AcrValues.MFA: 1, AcrValues.PHR: 2}

# Values from other providers that Kinde reads as mfa. Only relevant for values
# passed through auth_params; the SDK's own options send mfa or phr only.
_ACR_ALIASES = {
    "http://schemas.openid.net/pape/policies/2007/06/multi-factor": AcrValues.MFA,
    "urn:okta:loa:2fa:any": AcrValues.MFA,
}

_DIGITS = re.compile(r"[0-9]+")


def _split_acr_values(acr_values: Any) -> List[str]:
    """Split a string or a list/tuple of strings into individual acr values."""
    if isinstance(acr_values, str):
        return acr_values.split()
    if isinstance(acr_values, (list, tuple)):
        parts: List[str] = []
        for value in acr_values:
            if not isinstance(value, str):
                raise ValueError("acr_values must be a string or a list of strings")
            parts.extend(value.split())
        return parts
    raise ValueError("acr_values must be a string or a list of strings")


def normalize_acr_values(acr_values: AcrInput) -> str:
    """
    Validate ``acr_values`` and return the space-separated string to send.

    Args:
        acr_values: ``"mfa"``, ``"phr"``, a space-separated string, or a list of them.

    Returns:
        The lower-cased, de-duplicated, space-separated value (e.g. ``"mfa phr"``).

    Raises:
        ValueError: If the value is empty, not a string or list of strings, or
            contains anything other than ``mfa`` or ``phr``. Kinde silently
            ignores values it doesn't recognise, which would skip the step-up.
    """
    parts = _split_acr_values(acr_values)
    if not parts:
        raise ValueError("acr_values must not be empty. Expected 'mfa' or 'phr'")

    normalized: List[str] = []
    for part in parts:
        value = part.lower()
        if value not in _ACR_RANK:
            raise ValueError(f"Unsupported acr value {part!r}. Expected 'mfa' or 'phr'")
        if value not in normalized:
            normalized.append(value)
    return " ".join(normalized)


def normalize_max_age(max_age: int) -> int:
    """
    Validate ``max_age`` (seconds since the user last authenticated).

    Raises:
        ValueError: If the value is not a non-negative ``int``. ``bool`` and
            ``float`` are rejected, including ``True`` and ``300.0``.
    """
    if isinstance(max_age, bool) or not isinstance(max_age, int):
        raise ValueError(
            f"max_age must be a non-negative whole number of seconds (int), got {max_age!r}"
        )
    if max_age < 0:
        raise ValueError(f"max_age must not be negative, got {max_age!r}")
    return max_age


def normalize_step_up_auth_param(key: str, value: Any) -> Optional[str]:
    """
    Normalize an ``acr_values`` or ``max_age`` entry passed through ``auth_params``.

    ``auth_params`` is a raw passthrough, so this is more lenient than the typed
    login options: ``max_age`` may be a string of digits, and ``acr_values`` is
    not restricted to ``mfa`` / ``phr``. An unset value is never sent.

    Returns:
        The string to send, or ``None`` when the value is unset (``None`` or
        empty) and the parameter must be omitted.

    Raises:
        ValueError: If ``max_age`` is not a non-negative whole number (this
            includes the strings ``"undefined"``, ``"null"`` and ``"NaN"``), or
            ``acr_values`` is not a string or list of strings.
    """
    if value is None:
        return None

    if key == "max_age":
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return None
            if not _DIGITS.fullmatch(text):
                raise ValueError(
                    f"max_age must be a non-negative whole number of seconds, got {value!r}"
                )
            return str(int(text))
        return str(normalize_max_age(value))

    if key == "acr_values":
        parts = _split_acr_values(value)
        return " ".join(parts) if parts else None

    raise ValueError(f"{key!r} is not a step-up parameter")


def strongest_acr(acr_values: Optional[AcrInput]) -> Optional[str]:
    """
    Return the strongest context Kinde would apply for ``acr_values``.

    Kinde applies the highest recognised value and ignores the rest, so this
    returns ``"phr"``, ``"mfa"``, or ``None`` when nothing is recognised.
    """
    if acr_values is None:
        return None

    best: Optional[str] = None
    for part in _split_acr_values(acr_values):
        value = part.lower()
        value = _ACR_ALIASES.get(value, value)
        if value in _ACR_RANK and (best is None or _ACR_RANK[value] > _ACR_RANK[best]):
            best = value
    return best


def prompt_includes_none(prompt: Any) -> bool:
    """Whether a ``prompt`` value (string, enum or list) contains ``none``."""
    if prompt is None:
        return False
    if isinstance(prompt, Enum):
        prompt = prompt.value
    if isinstance(prompt, (list, tuple)):
        return any(prompt_includes_none(value) for value in prompt)
    return "none" in str(prompt).lower().split()


def discovery_supports_step_up(openid_configuration: Any) -> bool:
    """
    Whether a discovery document advertises step-up (``acr_values_supported``).

    When it doesn't, Kinde ignores ``acr_values`` and ``max_age``, tokens carry
    no ``acr`` or ``amr``, and ``auth_time`` may be the token's issue time.
    """
    if not isinstance(openid_configuration, Mapping):
        return False
    supported = openid_configuration.get("acr_values_supported")
    return isinstance(supported, (list, tuple)) and len(supported) > 0


def _claim_acr(claims: Mapping) -> Optional[str]:
    acr = claims.get("acr")
    return acr if isinstance(acr, str) and acr else None


def _claim_amr(claims: Mapping) -> Optional[List[str]]:
    amr = claims.get("amr")
    if isinstance(amr, (list, tuple)):
        return [value for value in amr if isinstance(value, str)]
    return None


def _claim_auth_time(claims: Mapping) -> Optional[int]:
    auth_time = claims.get("auth_time")
    if isinstance(auth_time, bool) or not isinstance(auth_time, (int, float)):
        return None
    return int(auth_time)


def authentication_context_from_claims(
    id_token_claims: Optional[Mapping] = None,
    access_token_claims: Optional[Mapping] = None,
    trust_auth_time: bool = True,
) -> Dict[str, Any]:
    """
    Build the authentication context from decoded token claims.

    ``auth_time`` is read from the ID token, because Kinde always sets it there
    and only sets it on the access token when it can establish it. The access
    token is the fallback for each claim.

    Args:
        id_token_claims: Claims of the session's ID token, if there is one.
        access_token_claims: Claims of the session's access token.
        trust_auth_time: Pass ``False`` when the environment doesn't advertise
            step-up. ``auth_time`` may then be the token's issue time, so it is
            reported as ``None`` instead.

    Returns:
        ``{"acr": "mfa" | "phr" | None, "amr": [...], "auth_time": int | None}``.
        ``acr`` is ``None`` for a single-factor sign-in.
    """
    id_claims = id_token_claims if isinstance(id_token_claims, Mapping) else {}
    access_claims = (
        access_token_claims if isinstance(access_token_claims, Mapping) else {}
    )

    # Tokens of two different users never describe one authentication
    id_sub = id_claims.get("sub")
    access_sub = access_claims.get("sub")
    if id_sub and access_sub and id_sub != access_sub:
        return {"acr": None, "amr": [], "auth_time": None}

    acr = _claim_acr(id_claims) or _claim_acr(access_claims)

    amr = _claim_amr(id_claims)
    if amr is None:
        amr = _claim_amr(access_claims) or []

    auth_time = None
    if trust_auth_time:
        auth_time = _claim_auth_time(id_claims)
        if auth_time is None:
            auth_time = _claim_auth_time(access_claims)

    return {"acr": acr, "amr": amr, "auth_time": auth_time}


def has_authentication_context(
    context: Mapping,
    acr: Optional[AcrInput] = None,
    max_age: Optional[int] = None,
    now: Optional[float] = None,
    leeway: int = 0,
) -> bool:
    """
    Check whether an authentication context meets a requirement.

    This is the single implementation of the check. ``OAuth.has_authentication_context``
    uses it for the current session, and it works equally on the claims of a
    token you have verified yourself (it only reads ``acr`` and ``auth_time``).
    ``amr`` is never used to decide: Kinde has already folded it into ``acr``.

    Args:
        context: A mapping with ``acr`` and ``auth_time``, such as the result of
            ``get_authentication_context()`` or verified token claims.
        acr: Required context, ``"mfa"`` or ``"phr"`` (``phr`` also meets ``mfa``).
        max_age: Maximum age of the last authentication, in seconds.
        now: Current time in seconds since the epoch. Defaults to ``time.time()``.
        leeway: Clock tolerance, in seconds, added to ``max_age``.

    Returns:
        ``True`` if the requirement is met. An absent ``acr`` meets no ``acr``
        requirement, and a missing ``auth_time`` meets no ``max_age`` requirement.

    Raises:
        ValueError: If ``acr`` or ``max_age`` is not a valid requirement.
    """
    if acr is not None:
        required = strongest_acr(normalize_acr_values(acr))
        actual = _claim_acr(context)
        if _ACR_RANK.get(actual.lower() if actual else "", 0) < _ACR_RANK[required]:
            return False

    if max_age is not None:
        max_age = normalize_max_age(max_age)
        auth_time = _claim_auth_time(context)
        if auth_time is None:
            return False
        if now is None:
            now = time.time()
        if now - auth_time > max_age + leeway:
            return False

    return True
