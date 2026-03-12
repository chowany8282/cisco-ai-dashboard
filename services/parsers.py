from __future__ import annotations

import re
from html import escape

PART_PATTERN = re.compile(
    r"\[PART_1\](?P<part1>.*?)\[PART_2\](?P<part2>.*?)\[PART_3\](?P<part3>.*)",
    re.DOTALL,
)


def parse_log_analysis(text: str) -> dict[str, str] | None:
    match = PART_PATTERN.search(text or "")
    if not match:
        return None
    return {
        "part1": match.group("part1").strip(),
        "part2": match.group("part2").strip(),
        "part3": match.group("part3").strip(),
    }


def sanitize_basic_html(raw_html: str) -> str:
    """Allow a small HTML subset used by this app and escape everything else."""
    if not raw_html:
        return ""

    allowed_tags = ["table", "tr", "th", "td", "a", "h3", "br"]

    escaped = escape(raw_html)

    # very lightweight unescape for known safe tags only
    for tag in allowed_tags:
        escaped = escaped.replace(f"&lt;{tag}&gt;", f"<{tag}>")
        escaped = escaped.replace(f"&lt;/{tag}&gt;", f"</{tag}>")
        escaped = escaped.replace(f"&lt;{tag} ", f"<{tag} ")

    # remove javascript: links (still escaped/unescaped mix safe-guard)
    escaped = escaped.replace("javascript:", "")
    return escaped
