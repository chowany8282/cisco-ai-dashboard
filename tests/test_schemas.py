from services.schemas import validate_log_analysis_json


def test_validate_log_analysis_json_success():
    raw = '{"part1":"원인","part2":"영향","part3":"조치"}'
    parsed = validate_log_analysis_json(raw)
    assert parsed is not None
    assert parsed.part1 == "원인"


def test_validate_log_analysis_json_failure():
    raw = '{"part1":"원인"}'
    assert validate_log_analysis_json(raw) is None
