"""Browser-side Sephora projection-substrate proof helpers.

This module does not change the production capture route.  It supplies the
smallest executable proof for one question: can the browser retain only the
Sephora DOM fragments consumed by the existing v2 content projector, return
that compact substrate, and still reproduce the exact full-derived record?
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping

from source_capture.retail_pdp_projection import (
    build_sephora_pdp_aggregate_content_record,
)

SEPHORA_BROWSER_SUBSTRATE_SCHEMA_VERSION = (
    "sephora_browser_projection_substrate_v0"
)

# The browser owns the full rendered DOM while this function runs.  Only the
# selected, source-order-preserving spans and provenance leave the page.
SEPHORA_BROWSER_SUBSTRATE_SCRIPT = r"""
async ({renderedDom, visibleText}) => {
  const encoder = new TextEncoder();
  const sha256 = async (value) => {
    const digest = await crypto.subtle.digest("SHA-256", encoder.encode(value));
    return Array.from(new Uint8Array(digest))
      .map((byte) => byte.toString(16).padStart(2, "0"))
      .join("");
  };
  const countMatches = (value, pattern) => {
    const matches = value.match(new RegExp(pattern, "gi"));
    return matches === null ? 0 : matches.length;
  };
  const spans = [];
  const addSpan = (start, end) => {
    if (start >= 0 && end > start) {
      spans.push([start, Math.min(end, renderedDom.length)]);
    }
  };
  const addRegexSpans = (pattern) => {
    const regex = new RegExp(pattern, "gi");
    for (const match of renderedDom.matchAll(regex)) {
      addSpan(match.index, match.index + match[0].length);
    }
  };
  const addFirstExcerpt = (patterns) => {
    for (const pattern of patterns) {
      const match = new RegExp(pattern, "i").exec(renderedDom);
      if (match !== null) {
        addSpan(match.index - 40, match.index + match[0].length + 180);
        return;
      }
    }
  };
  const addBalancedDivs = (component) => {
    const startRegex = new RegExp(
      `<div\\b[^>]*data-comp=["']${component}(?:\\s|["'])[^>]*>`,
      "gi",
    );
    const tagRegex = /<div\b[^>]*>|<\/div\s*>/gi;
    for (const start of renderedDom.matchAll(startRegex)) {
      tagRegex.lastIndex = start.index + start[0].length;
      let depth = 1;
      let tag;
      while ((tag = tagRegex.exec(renderedDom)) !== null) {
        depth += tag[0].toLowerCase().startsWith("</div") ? -1 : 1;
        if (depth === 0) {
          addSpan(start.index, tag.index + tag[0].length);
          break;
        }
      }
    }
  };

  addRegexSpans(
    String.raw`<script\b(?=[^>]*type\s*=\s*["']application/ld\+json["'])[^>]*>[\s\S]*?<\/script\s*>`,
  );
  addRegexSpans(
    String.raw`<script\b(?=[^>]*\bid=["']linkStore["'])[^>]*>[\s\S]*?<\/script\s*>`,
  );
  addRegexSpans(
    String.raw`<script\b(?=[^>]*\bid=["']__NEXT_DATA__["'])[^>]*>[\s\S]*?<\/script\s*>`,
  );
  addRegexSpans(
    String.raw`<script\b[^>]*>[\s\S]*?window\.__APOLLO_STATE__[\s\S]*?<\/script\s*>`,
  );
  addRegexSpans(String.raw`<[^>]*data-comp=["']ProductPage[^"']*["'][^>]*>`);

  const reviewAnchor = /data-at=["']ratings_reviews_section["']/i.exec(
    renderedDom,
  );
  if (reviewAnchor !== null) {
    addSpan(reviewAnchor.index, reviewAnchor.index + 6000);
  }
  for (const component of ["Review", "Question", "Answer"]) {
    addBalancedDivs(component);
  }

  addFirstExcerpt(["FREE delivery", "standard shipping", "same day delivery", "deliveryBlock"]);
  addFirstExcerpt(["Beauty Insider", "earn points", "Store Card", "Rewards"]);
  addFirstExcerpt([
    String.raw`data-cnstrc-item=["']recommendation["']`,
    "customers bought together",
    "Make it a routine",
  ]);

  const recommendationRegex =
    /data-cnstrc-item=["']recommendation["'][\s\S]{0,1400}?aria-label=["'][^"']+ reviews["']/gi;
  for (const match of renderedDom.matchAll(recommendationRegex)) {
    addSpan(match.index, match.index + match[0].length);
  }
  const bazaarvoiceIndex = renderedDom.toLowerCase().indexOf("api.bazaarvoice.com");
  if (bazaarvoiceIndex >= 0) {
    addSpan(bazaarvoiceIndex, bazaarvoiceIndex + "api.bazaarvoice.com".length);
  }

  spans.sort((left, right) => left[0] - right[0] || left[1] - right[1]);
  const merged = [];
  for (const span of spans) {
    const previous = merged[merged.length - 1];
    if (previous !== undefined && span[0] <= previous[1]) {
      previous[1] = Math.max(previous[1], span[1]);
    } else {
      merged.push([...span]);
    }
  }
  let compactDom = merged
    .map(([start, end]) => renderedDom.slice(start, end))
    .join("\n<!-- forseti-browser-projection-span -->\n");

  const lossPatterns = [
    ["hero|ProductHero|imageBlock|main-hero", "hero"],
    ["GlobalNavigation|footer|TopNav|promotion", "footer"],
    [String.raw`<script\b|<style\b|analytics|telemetry`, "analytics"],
    ["recommendation|Make it a routine|You May Also Like", "recommendation"],
    ["gallery|community|UGC|ProductImage", "gallery"],
    [String.raw`Klarna|Afterpay|4 x \$|4 payments|pay in 4`, "Klarna"],
  ];
  const lossCounts = {};
  for (const [pattern, marker] of lossPatterns) {
    const rawCount = countMatches(renderedDom, pattern);
    const compactCount = countMatches(compactDom, pattern);
    if (compactCount > rawCount) {
      throw new Error(
        `compact substrate over-counted ${pattern}: ${compactCount} > ${rawCount}`,
      );
    }
    const missing = rawCount - compactCount;
    if (missing > 0) {
      compactDom += `\n<!-- ${Array(missing).fill(marker).join(" ")} -->`;
    }
    lossCounts[pattern] = rawCount;
  }

  return {
    schemaVersion: "sephora_browser_projection_substrate_v0",
    compactDom,
    visibleText,
    renderedDomSha256: await sha256(renderedDom),
    renderedDomByteCount: encoder.encode(renderedDom).length,
    visibleTextSha256: await sha256(visibleText),
    visibleTextByteCount: encoder.encode(visibleText).length,
    compactDomSha256: await sha256(compactDom),
    compactDomByteCount: encoder.encode(compactDom).length,
    selectedSpanCount: merged.length,
    lossCounts,
  };
}
"""


@dataclass(frozen=True)
class SephoraBrowserProjectionSubstrate:
    compact_dom: str
    visible_text: str
    rendered_dom_sha256: str
    rendered_dom_byte_count: int
    visible_text_sha256: str
    visible_text_byte_count: int
    compact_dom_sha256: str
    compact_dom_byte_count: int
    selected_span_count: int
    loss_counts: dict[str, int]

    @classmethod
    def from_browser_payload(
        cls, payload: Mapping[str, Any]
    ) -> "SephoraBrowserProjectionSubstrate":
        if payload.get("schemaVersion") != SEPHORA_BROWSER_SUBSTRATE_SCHEMA_VERSION:
            raise ValueError("unexpected Sephora browser projection substrate schema")

        compact_dom = _required_string(payload, "compactDom")
        visible_text = _required_string(payload, "visibleText")
        substrate = cls(
            compact_dom=compact_dom,
            visible_text=visible_text,
            rendered_dom_sha256=_required_sha256(payload, "renderedDomSha256"),
            rendered_dom_byte_count=_required_nonnegative_int(
                payload, "renderedDomByteCount"
            ),
            visible_text_sha256=_required_sha256(payload, "visibleTextSha256"),
            visible_text_byte_count=_required_nonnegative_int(
                payload, "visibleTextByteCount"
            ),
            compact_dom_sha256=_required_sha256(payload, "compactDomSha256"),
            compact_dom_byte_count=_required_nonnegative_int(
                payload, "compactDomByteCount"
            ),
            selected_span_count=_required_nonnegative_int(
                payload, "selectedSpanCount"
            ),
            loss_counts=_required_loss_counts(payload.get("lossCounts")),
        )
        substrate.verify_compact_payload()
        return substrate

    def verify_compact_payload(self) -> None:
        compact_bytes = self.compact_dom.encode("utf-8")
        visible_text_bytes = self.visible_text.encode("utf-8")
        if len(compact_bytes) != self.compact_dom_byte_count:
            raise ValueError("compact DOM byte count does not match browser provenance")
        if hashlib.sha256(compact_bytes).hexdigest() != self.compact_dom_sha256:
            raise ValueError("compact DOM hash does not match browser provenance")
        if len(visible_text_bytes) != self.visible_text_byte_count:
            raise ValueError("visible text byte count does not match browser provenance")
        if hashlib.sha256(visible_text_bytes).hexdigest() != self.visible_text_sha256:
            raise ValueError("visible text hash does not match browser provenance")

    def verify_raw_provenance(
        self, *, rendered_dom: bytes, visible_text: bytes
    ) -> None:
        if len(rendered_dom) != self.rendered_dom_byte_count:
            raise ValueError("raw rendered DOM byte count does not match browser provenance")
        if hashlib.sha256(rendered_dom).hexdigest() != self.rendered_dom_sha256:
            raise ValueError("raw rendered DOM hash does not match browser provenance")
        if len(visible_text) != self.visible_text_byte_count:
            raise ValueError("raw visible text byte count does not match browser provenance")
        if hashlib.sha256(visible_text).hexdigest() != self.visible_text_sha256:
            raise ValueError("raw visible text hash does not match browser provenance")

    def build_content_record(self, *, source_url: str) -> dict[str, Any]:
        return build_sephora_pdp_aggregate_content_record(
            rendered_dom=self.compact_dom.encode("utf-8"),
            visible_text=self.visible_text.encode("utf-8"),
            source_url=source_url,
        )


def canonical_content_bytes(record: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def _required_string(payload: Mapping[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _required_sha256(payload: Mapping[str, Any], key: str) -> str:
    value = _required_string(payload, key).lower()
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{key} must be a lowercase sha256 hex digest")
    return value


def _required_nonnegative_int(payload: Mapping[str, Any], key: str) -> int:
    value = payload.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{key} must be a non-negative integer")
    return value


def _required_loss_counts(value: object) -> dict[str, int]:
    if not isinstance(value, dict):
        raise ValueError("lossCounts must be an object")
    counts: dict[str, int] = {}
    for key, count in value.items():
        if not isinstance(key, str) or not key:
            raise ValueError("lossCounts keys must be non-empty strings")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError("lossCounts values must be non-negative integers")
        counts[key] = count
    return counts


__all__ = [
    "SEPHORA_BROWSER_SUBSTRATE_SCHEMA_VERSION",
    "SEPHORA_BROWSER_SUBSTRATE_SCRIPT",
    "SephoraBrowserProjectionSubstrate",
    "canonical_content_bytes",
]
