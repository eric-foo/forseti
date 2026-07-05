from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Iterable


@dataclass
class HtmlNode:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list["HtmlNode"] = field(default_factory=list)
    text_parts: list[str] = field(default_factory=list)
    parent: "HtmlNode | None" = None

    def classes(self) -> set[str]:
        return {item for item in self.attrs.get("class", "").split() if item}

    def has_class(self, class_name: str) -> bool:
        return class_name in self.classes()

    def text_content(self) -> str:
        parts: list[str] = []
        self._collect_text(parts)
        return " ".join(" ".join(parts).split())

    def descendants(self) -> Iterable["HtmlNode"]:
        for child in self.children:
            yield child
            yield from child.descendants()

    def first_descendant(self, *, tag: str | None = None, class_name: str | None = None) -> "HtmlNode | None":
        for node in self.descendants():
            if tag is not None and node.tag != tag:
                continue
            if class_name is not None and not node.has_class(class_name):
                continue
            return node
        return None

    def _collect_text(self, parts: list[str]) -> None:
        parts.extend(part.strip() for part in self.text_parts if part.strip())
        for child in self.children:
            child._collect_text(parts)


class _DomBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = HtmlNode(tag="document")
        self._stack: list[HtmlNode] = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = HtmlNode(
            tag=tag.lower(),
            attrs={key.lower(): value or "" for key, value in attrs},
            parent=self._stack[-1],
        )
        self._stack[-1].children.append(node)
        if tag.lower() not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param"}:
            self._stack.append(node)

    def handle_endtag(self, tag: str) -> None:
        normalized = tag.lower()
        for index in range(len(self._stack) - 1, 0, -1):
            if self._stack[index].tag == normalized:
                del self._stack[index:]
                return

    def handle_data(self, data: str) -> None:
        if data:
            self._stack[-1].text_parts.append(data)


def parse_html_document(html: str) -> HtmlNode:
    builder = _DomBuilder()
    builder.feed(html)
    builder.close()
    return builder.root
