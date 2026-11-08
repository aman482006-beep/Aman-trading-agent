import pytest

from agent_lab.earnings_intelligence.pipeline import Chunk, Claim, build_claim, retrieve


def sample_chunks():
    return [
        Chunk("guidance", "Cloud revenue growth guidance remains above twenty percent.", "guidance"),
        Chunk("margin", "Operating margin expanded year over year.", "financials"),
        Chunk("risk", "Customer acquisition costs remain a near-term risk.", "risks"),
    ]


def test_retrieve_ranks_lexical_overlap_and_preserves_tie_order():
    chunks = sample_chunks()
    results = retrieve(chunks, "revenue growth", top_k=2)

    assert [chunk.id for chunk in results] == ["guidance"]


def test_retrieve_returns_empty_for_query_without_tokens():
    assert retrieve(sample_chunks(), "AI") == []


@pytest.mark.parametrize("query", ["", "   ", None])
def test_retrieve_rejects_empty_or_invalid_query(query):
    with pytest.raises(ValueError, match="query"):
        retrieve(sample_chunks(), query)


@pytest.mark.parametrize("top_k", [0, -1, True, 1.5, "2"])
def test_retrieve_rejects_invalid_top_k(top_k):
    with pytest.raises(ValueError, match="top_k"):
        retrieve(sample_chunks(), "revenue", top_k=top_k)


def test_retrieve_rejects_invalid_chunk_sequence():
    with pytest.raises(ValueError, match="Chunk records"):
        retrieve("not chunks", "growth")
    with pytest.raises(ValueError, match="only Chunk records"):
        retrieve([{"id": "x"}], "growth")


@pytest.mark.parametrize(
    "chunk_id,text,section",
    [("", "text", "section"), ("id", " ", "section"), ("id", "text", "")],
)
def test_chunk_requires_non_empty_fields(chunk_id, text, section):
    with pytest.raises(ValueError, match="non-empty"):
        Chunk(chunk_id, text, section)


def test_build_claim_attaches_evidence_ids_and_heuristic_score():
    evidence = retrieve(sample_chunks(), "revenue growth")
    claim = build_claim("Growth guidance remains positive.", evidence)

    assert claim.evidence_ids == ["guidance"]
    assert claim.confidence == 0.65


def test_build_claim_without_evidence_has_zero_confidence():
    claim = build_claim("No evidence found.", [])
    assert claim.evidence_ids == []
    assert claim.confidence == 0.0


def test_build_claim_rejects_invalid_inputs():
    with pytest.raises(ValueError, match="summary"):
        build_claim(" ", [])
    with pytest.raises(ValueError, match="evidence"):
        build_claim("A claim.", "not evidence")
    with pytest.raises(ValueError, match="confidence"):
        Claim("claim", [], 1.5)


def test_claim_rejects_oversized_integer_confidence():
    with pytest.raises(ValueError, match="confidence"):
        Claim("claim", [], 10 ** 1000)
