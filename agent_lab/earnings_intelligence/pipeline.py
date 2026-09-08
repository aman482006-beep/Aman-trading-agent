from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str
    section: str


@dataclass(frozen=True)
class Claim:
    text: str
    evidence_ids: List[str]
    confidence: float


def retrieve(chunks: List[Chunk], query: str, top_k: int = 3) -> List[Chunk]:
    """Tiny transparent retrieval baseline; replace with embeddings without changing the agent contract."""
    terms = {term.lower() for term in query.split() if len(term) > 2}
    ranked = []
    for chunk in chunks:
        score = sum(term in chunk.text.lower() for term in terms)
        if score:
            ranked.append((score, chunk))
    return [chunk for _, chunk in sorted(ranked, key=lambda item: item[0], reverse=True)[:top_k]]


def build_claim(summary: str, evidence: List[Chunk]) -> Claim:
    """Force a generated conclusion to carry explicit evidence references."""
    if not evidence:
        return Claim(summary, [], 0.0)
    confidence = min(0.95, 0.55 + 0.10 * len(evidence))
    return Claim(summary, [chunk.id for chunk in evidence], round(confidence, 2))
