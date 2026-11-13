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
from typing import Any, List, Optional, Union


class AcrValues:
    """Authentication contexts that Kinde recognises in ``acr_values``."""

    MFA = "mfa"  # A second factor
    PHR = "phr"  # Phishing-resistant (a passkey with user verification); also meets MFA


AcrInput = Union[str, List[str], tuple]

# phr meets an mfa requirement; an absent acr ranks 0
_ACR_RANK = {AcrValues.MFA: 1, AcrValues.PHR: 2}

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
