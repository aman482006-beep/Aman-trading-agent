from __future__ import annotations

import re
from dataclasses import dataclass
from math import isfinite
from typing import List, Sequence


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.casefold())
        if len(token) > 2
    }


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str
    section: str

    def __post_init__(self) -> None:
        for field_name, value in (("id", self.id), ("text", self.text), ("section", self.section)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"chunk {field_name} must be a non-empty string")


@dataclass(frozen=True)
class Claim:
    text: str
    evidence_ids: List[str]
    confidence: float

    def __post_init__(self) -> None:
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("claim text must be a non-empty string")
        if not isinstance(self.evidence_ids, list) or any(
            not isinstance(item, str) or not item.strip() for item in self.evidence_ids
        ):
            raise ValueError("evidence_ids must be a list of non-empty strings")
        if (
            isinstance(self.confidence, bool)
            or not isinstance(self.confidence, (int, float))
            or not isfinite(self.confidence)
            or not 0.0 <= self.confidence <= 1.0
        ):
            raise ValueError("confidence must be a finite value between 0 and 1")


def retrieve(chunks: Sequence[Chunk], query: str, top_k: int = 3) -> List[Chunk]:
    """Rank supplied chunks by transparent lexical token overlap.

    This is a small baseline, not semantic search. Ranking ties preserve input order.
    """
    if not isinstance(chunks, Sequence) or isinstance(chunks, (str, bytes)):
        raise ValueError("chunks must be a sequence of Chunk records")
    if any(not isinstance(chunk, Chunk) for chunk in chunks):
        raise ValueError("chunks must contain only Chunk records")
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a non-empty string")
    if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k < 1:
        raise ValueError("top_k must be a positive integer")

    query_terms = _tokens(query)
    if not query_terms:
        return []

    ranked = []
    for index, chunk in enumerate(chunks):
        score = len(query_terms.intersection(_tokens(chunk.text)))
        if score:
            ranked.append((score, index, chunk))

    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [chunk for _, _, chunk in ranked[:top_k]]


def build_claim(summary: str, evidence: Sequence[Chunk]) -> Claim:
    """Attach evidence IDs to a supplied summary.

    The confidence value is a simple evidence-count heuristic, not a calibrated
    probability and not a score produced by a language model.
    """
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError("summary must be a non-empty string")
    if not isinstance(evidence, Sequence) or isinstance(evidence, (str, bytes)):
        raise ValueError("evidence must be a sequence of Chunk records")
    if any(not isinstance(chunk, Chunk) for chunk in evidence):
        raise ValueError("evidence must contain only Chunk records")

    if not evidence:
        return Claim(summary.strip(), [], 0.0)

    confidence = min(0.95, 0.55 + 0.10 * len(evidence))
    return Claim(
        summary.strip(),
        [chunk.id for chunk in evidence],
        round(confidence, 2),
    )
