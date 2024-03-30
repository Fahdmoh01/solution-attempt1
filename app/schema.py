from pydantic import BaseModel, Field, validator
from typing import Optional, Union


class PasswordFields(BaseModel):
    length: int = Field(default=12)
    symbols: Optional[bool] = Field(default=True)
    digits: Optional[bool] = Field(default=True)
    lowercase: Optional[bool] = Field(default=True)
    uppercase: Optional[bool] = Field(default=True)

    @validator("length")
    def verify_length(cls, lengthCheck: int) -> int:
        if lengthCheck <= 0:
            raise ValueError("length must be a positive integer")
        return lengthCheck
