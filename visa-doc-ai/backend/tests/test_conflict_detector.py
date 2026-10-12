from app.verification.conflict_detector import ConflictDetector
from app.schemas.requirement import ExtractedEvidence


def test_conflict_detection_bank_statements():
    ev_a = ExtractedEvidence(
        id="ev_a",
        source_id="src_a",
        source_url="https://india.diplo.de/bank-reqs",
        source_title="German Embassy India",
        is_official=True,
        exact_quote="Applicants must provide personal bank statements covering the last 3 months stamped by the bank."
    )
    ev_b = ExtractedEvidence(
        id="ev_b",
        source_id="src_b",
        source_url="https://generic-travel.com/schengen-financial",
        source_title="Travel Blog Guide",
        is_official=False,
        exact_quote="You must submit your bank statements for the last 6 months to prove sufficient funds."
    )
    
    conflicts = ConflictDetector.detect_conflicts([ev_a, ev_b])
    assert len(conflicts) >= 1
    conflict = conflicts[0]
    assert "Bank Statement Duration" in conflict.requirement_title
    assert "3 months" in conflict.issue
    assert "6 months" in conflict.issue
    assert "Official source" in conflict.resolution_strategy
