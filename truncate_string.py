from typing import Callable


def DEFAULT_AFTER(max_length: int, more: int) -> str:
    return f'... (truncated - {more} more)' if max_length >= 1000 else '...'


def truncate(
    string: str,
    *,
    max_length: int,
    after: str | Callable[[int, int], str] = DEFAULT_AFTER,
) -> str:
    if len(string) <= max_length:
        return string
    after = after(max_length, len(string) - max_length) if callable(after) else after
    return string[:max_length - len(after)] + after
