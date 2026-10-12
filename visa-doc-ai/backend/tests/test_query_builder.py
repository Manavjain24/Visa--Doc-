from app.search.query_builder import QueryBuilder
from app.schemas.visa_profile import ApplicantProfile


def test_query_builder_generates_targeted_tasks(sample_profile: ApplicantProfile):
    tasks = QueryBuilder.build_initial_tasks(sample_profile, user_question="Is flight ticket mandatory?")
    
    assert len(tasks) >= 2
    # Verify destination and category are present
    assert any("germany" in t.query.lower() for t in tasks)
    assert any("tourist" in t.query.lower() for t in tasks)
    assert any("checklist" in t.query.lower() for t in tasks)
    assert any("flight ticket" in t.query.lower() for t in tasks)
    
    # Priority check
    for t in tasks:
        assert t.priority in [1, 2]
        assert len(t.objective) > 0


def test_query_builder_gap_queries(sample_profile: ApplicantProfile):
    gaps = ["What is the health insurance minimum coverage?", "Are bank statements required for 3 or 6 months?"]
    gap_tasks = QueryBuilder.build_gap_queries(sample_profile, gaps)
    
    assert len(gap_tasks) == 2
    assert "health insurance" in gap_tasks[0].query.lower()
    assert "bank statements" in gap_tasks[1].query.lower()
