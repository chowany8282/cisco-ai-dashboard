from __future__ import annotations

import re
from html.parser import HTMLParser

PART_PATTERN = re.compile(
    r"\[PART_1\](?P<part1>.*?)\[PART_2\](?P<part2>.*?)\[PART_3\](?P<part3>.*)",
    re.DOTALL,
)


_ALLOWED_TAGS = {"table", "tr", "th", "td", "a", "h3", "br"}
_ALLOWED_ATTRS = {
    "a": {"href", "target", "rel"},
}


def parse_log_analysis(text: str) -> dict[str, str] | None:
    match = PART_PATTERN.search(text or "")
    if not match:
        return None
    return {
        "part1": match.group("part1").strip(),
        "part2": match.group("part2").strip(),
        "part3": match.group("part3").strip(),
    }


class _SafeHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in _ALLOWED_TAGS:
            return

        attr_parts: list[str] = []
        for key, value in attrs:
            if key not in _ALLOWED_ATTRS.get(tag, set()):
                continue
            safe_val = (value or "").strip()
            if key == "href":
                if not safe_val.startswith(("https://", "http://")):
                    continue
            if "javascript:" in safe_val.lower() or "data:" in safe_val.lower():
                continue
            attr_parts.append(f'{key}="{safe_val}"')

        if tag == "a":
            if not any(part.startswith("target=") for part in attr_parts):
                attr_parts.append('target="_blank"')
            if not any(part.startswith("rel=") for part in attr_parts):
                attr_parts.append('rel="noopener noreferrer"')

        attrs_joined = f" {' '.join(attr_parts)}" if attr_parts else ""
        self.chunks.append(f"<{tag}{attrs_joined}>")

    def handle_endtag(self, tag: str) -> None:
        if tag in _ALLOWED_TAGS and tag != "br":
            self.chunks.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        self.chunks.append(data)


def sanitize_basic_html(raw_html: str) -> str:
    if not raw_html:
        return ""

    parser = _SafeHTMLParser()
    parser.feed(raw_html)
    parser.close()
    return "".join(parser.chunks)
