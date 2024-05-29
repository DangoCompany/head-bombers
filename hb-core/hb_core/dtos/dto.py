from typing import Optional, Tuple

from pydantic import BaseModel, Field


class GetLatestUpdateDateReturnValue(BaseModel):
    error_codes: Tuple[int, ...] = Field(..., title="Error Codes")
    date: Optional[str] = Field(None, description="Latest Update Date")


class PostImageReturnValue(BaseModel):
    error_codes: Tuple[int, ...] = Field(..., title="Error Codes")


class CalculateParameterReturnValue(BaseModel):
    error_codes: Tuple[int, ...] = Field(..., title="Error Codes")
    parameter: float = Field(0, description="Parameter")
