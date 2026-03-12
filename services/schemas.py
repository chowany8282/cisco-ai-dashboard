from __future__ import annotations

import json
import re
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class LogAnalysisResult(BaseModel):
    part1: str = Field(min_length=1, description="발생 원인")
    part2: str = Field(min_length=1, description="네트워크 영향")
    part3: str = Field(min_length=1, description="조치 방법")


_JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)


def extract_json_object(text: str) -> dict[str, Any] | None:
    if not text:
        return None
    match = _JSON_BLOCK_RE.search(text)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def validate_log_analysis_json(text: str) -> LogAnalysisResult | None:
    payload = extract_json_object(text)
    if not payload:
        return None
    try:
        return LogAnalysisResult.model_validate(payload)
    except ValidationError:
        return None
