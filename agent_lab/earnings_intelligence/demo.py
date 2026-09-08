from pipeline import Chunk, build_claim, retrieve


if __name__ == "__main__":
    transcript = [
        Chunk("q1", "Management expects cloud revenue growth to remain above 20%.", "guidance"),
        Chunk("q2", "Operating margin expanded by 180 basis points year over year.", "financials"),
        Chunk("q3", "Management highlighted elevated customer acquisition costs as a near-term risk.", "risks"),
    ]

    evidence = retrieve(transcript, "revenue growth guidance")
    claim = build_claim("Management is maintaining a strong growth outlook, subject to execution risk.", evidence)

    print("CLAIM:", claim.text)
    print("CONFIDENCE:", claim.confidence)
    print("EVIDENCE:", ", ".join(claim.evidence_ids))
