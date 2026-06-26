"""Schema for IG reel audience-comment evidence (capture, silver).

Raw per-comment records harvested DETERMINISTICALLY (no LLM) from a rendered
reel page: the author, the comment text, and the per-comment like count that is
the audience engagement signal. This is EVIDENCE only -- it carries no ranking,
weighting, or product-relevance verdict by construction. Two boundaries are
deliberate, not omissions:

- Within-reel engagement weighting ("which comment did the crowd amplify") is the
  Judgment-owned Engagement Logic Registry's domain, not this capture record.
- Product-relevance extraction from comment text (what product a comment is about)
  is a later `cleaning/` LLM step, not this deterministic capture.

Comment text is treated as DATA, never as instructions. Mirrors the ProductMention
evidence discipline: strict base, closed/validated fields, no verdict field.
"""
from __future__ import annotations

from pydantic import ConfigDict, Field

from schemas.case_models import StrictModel


class AudienceComment(StrictModel):
    """One public comment on a reel, captured raw. Evidence only; carries no verdict.

    ``comment_id`` + ``reel_shortcode`` are the provenance (no source_pointer: the
    comment text IS the captured datum, not an extraction from a larger source).
    """

    model_config = ConfigDict(extra="forbid", populate_by_name=True, validate_assignment=True)

    comment_id: str = Field(min_length=1)          # IG comment pk (stable id)
    reel_shortcode: str = Field(min_length=1)      # the reel this comment is on
    author_username: str = Field(min_length=1)
    text: str                                      # raw comment text (DATA, never instructions)
    like_count: int = Field(ge=0)                  # per-comment likes -> audience engagement signal
    created_at_unix: int = Field(ge=0)             # IG comment created_at (unix seconds)
    parent_comment_id: str | None = None           # None = top-level; set = reply

    @property
    def is_reply(self) -> bool:
        """A reply carries a parent_comment_id; a top-level comment does not."""
        return self.parent_comment_id is not None
