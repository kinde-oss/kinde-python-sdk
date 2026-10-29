"""
Building and parsing ``WWW-Authenticate`` headers (RFC 9110 §11.6.1, RFC 6750 §3).
"""

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple, Union

_TOKEN_CHARS = frozenset("!#$%&'*+-.^_`|~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
_TOKEN68_EXTRA = frozenset("/")


def quote(value: str) -> str:
    """Return ``value`` as an RFC 9110 quoted-string, escaping ``"`` and ``\\``."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_challenge(scheme: str = "Bearer", params: Union[Dict[str, str], Iterable[Tuple[str, str]]] = ()) -> str:
    """Build one challenge, quoting every parameter value. ``None`` values are skipped."""
    items = params.items() if isinstance(params, dict) else params
    rendered = ", ".join(f"{name}={quote(value)}" for name, value in items if value is not None)
    return f"{scheme} {rendered}" if rendered else scheme


@dataclass
class Challenge:
    scheme: str
    params: Dict[str, str] = field(default_factory=dict)  # names lower-cased
    token68: Optional[str] = None

    def get(self, name: str) -> Optional[str]:
        return self.params.get(name.lower())


class _Scanner:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def peek(self) -> str:
        """Return the current character, or an empty string at the end."""
        return self.text[self.pos] if self.pos < len(self.text) else ""

    def skip_spaces(self) -> None:
        """Skip spaces and tabs."""
        while self.peek() in (" ", "\t"):
            self.pos += 1

    def skip_separators(self) -> None:
        """Skip spaces, tabs and commas."""
        while self.peek() in (" ", "\t", ","):
            self.pos += 1

    def token(self, extra=frozenset()) -> str:
        """Read an RFC 7230 token, also accepting the characters in ``extra``."""
        start = self.pos
        while self.peek() and (self.peek() in _TOKEN_CHARS or self.peek() in extra):
            self.pos += 1
        return self.text[start : self.pos]

    def quoted_string(self) -> str:
        """Read a quoted string, unescaping backslashes."""
        # Assumes the opening quote is at self.pos. An unterminated string runs to the end.
        self.pos += 1
        chars = []
        while self.pos < len(self.text):
            char = self.text[self.pos]
            if char == "\\" and self.pos + 1 < len(self.text):
                chars.append(self.text[self.pos + 1])
                self.pos += 2
                continue
            self.pos += 1
            if char == '"':
                break
            chars.append(char)
        return "".join(chars)


def parse_www_authenticate(headers: Union[str, Iterable[str], None]) -> List[Challenge]:
    """Parse one or more ``WWW-Authenticate`` header values into challenges.

    Handles several challenges in one header, quoted strings with escaped quotes,
    commas inside quotes, token68 credentials and case-insensitive names.
    Malformed input yields the challenges that could be read, never an exception.
    """
    if headers is None:
        return []
    values = [headers] if isinstance(headers, str) else list(headers)
    challenges: List[Challenge] = []
    for value in values:
        challenges.extend(_parse_one(value))
    return challenges


def _parse_one(text: str) -> List[Challenge]:
    """Parse one header value into its challenges."""
    scanner = _Scanner(text)
    challenges: List[Challenge] = []
    current: Optional[Challenge] = None
    while True:
        scanner.skip_separators()
        if not scanner.peek():
            break
        name = scanner.token()
        if not name:
            # Not a token: skip one character so malformed input can't loop forever
            scanner.pos += 1
            continue
        scanner.skip_spaces()
        if scanner.peek() == "=":
            scanner.pos += 1
            scanner.skip_spaces()
            value = scanner.quoted_string() if scanner.peek() == '"' else scanner.token()
            if current is not None:  # a parameter before any scheme is ignored
                current.params[name.lower()] = value
            continue
        current = Challenge(scheme=name)
        challenges.append(current)
        current.token68 = _read_token68(scanner)
    return challenges


def _read_token68(scanner: _Scanner) -> Optional[str]:
    """Read a token68 right after a scheme, or leave the position unchanged when there is none."""
    start = scanner.pos
    scanner.token(_TOKEN68_EXTRA)
    while scanner.peek() == "=":
        scanner.pos += 1
    candidate = scanner.text[start : scanner.pos]
    end = scanner.pos
    scanner.skip_spaces()
    # A token68 stands alone. "name=value" (something follows the "=") is a parameter instead.
    if candidate and scanner.peek() in ("", ","):
        scanner.pos = end
        return candidate
    scanner.pos = start
    return None


def find_bearer_challenge(headers: Union[str, Iterable[str], None]) -> Optional[Challenge]:
    """Return the first ``Bearer`` challenge, comparing the scheme case-insensitively."""
    for challenge in parse_www_authenticate(headers):
        if challenge.scheme.lower() == "bearer":
            return challenge
    return None
