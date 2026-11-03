from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class SurveySubmission(BaseModel):
    lang: str = Field(default="ko", pattern="^(ko|en)$")
    company_name: str = Field(..., min_length=1, max_length=200)
    country: str = Field(..., min_length=1, max_length=100)

    # 총괄 만족도 (1~5)
    q1_overall: Optional[int] = Field(None, ge=1, le=5)

    # 1. Invest KOREA 컨퍼런스
    conf_q1: Optional[int] = Field(None, ge=1, le=5)
    conf_q2: Optional[List[str]] = Field(default_factory=list)  # ["1", "2"]
    conf_q3_rank1: Optional[int] = Field(None, ge=1, le=6)
    conf_q3_rank2: Optional[int] = Field(None, ge=1, le=6)
    conf_q3_rank3: Optional[int] = Field(None, ge=1, le=6)
    conf_q3_other: Optional[str] = Field(None, max_length=500)
    conf_q4: Optional[str] = Field(None, max_length=2000)

    # 2. 지자체 투자환경 IR
    reg_q1: Optional[int] = Field(None, ge=1, le=5)
    reg_q2: Optional[int] = Field(None, ge=1, le=5)
    reg_q3_rank1: Optional[int] = Field(None, ge=1, le=5)
    reg_q3_rank2: Optional[int] = Field(None, ge=1, le=5)
    reg_q3_other: Optional[str] = Field(None, max_length=500)

    # 3. 외투 환경 세미나
    semi_q1: Optional[int] = Field(None, ge=1, le=5)
    semi_q2: Optional[List[str]] = Field(default_factory=list)
    semi_q3: Optional[str] = Field(None, max_length=2000)

    # 4. M.AX 에너지 전략 포럼
    max_q1: Optional[int] = Field(None, ge=1, le=5)
    max_q2: Optional[List[str]] = Field(default_factory=list)
    max_q3: Optional[str] = Field(None, max_length=2000)

    # 5. 글로벌 VC 스타트업 포럼
    vc_q1: Optional[int] = Field(None, ge=1, le=5)
    vc_q2: Optional[List[str]] = Field(default_factory=list)
    vc_q3: Optional[str] = Field(None, max_length=2000)

    @field_validator("company_name", "country")
    @classmethod
    def strip_strings(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Field cannot be empty or blank")
        return s


class SubmissionResponse(BaseModel):
    success: bool
    id: int
    message: str

