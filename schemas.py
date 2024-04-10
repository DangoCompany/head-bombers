from typing import Tuple, Optional

from pydantic import BaseModel, Field


class CalculateParameterReturnValue(BaseModel):
    error_codes: Tuple[int, ...] = Field(..., title="エラーコード")
    parameter: float = Field(0, description="パラメータ")


class GetLatestUpdateDateReturnValue(BaseModel):
    date: Optional[str] = Field(None, description="最終更新日時")
