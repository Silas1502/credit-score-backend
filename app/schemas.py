from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class CreditInput(BaseModel):

    income: float = Field(..., gt=0, description="Annual income")

    age: int = Field(..., ge=18, le=100)

    employment_years: int = Field(..., ge=0, le=60)

    loan_amount: float = Field(..., gt=0)

    loan_term: int = Field(..., ge=1, le=360)

    credit_history_length: int = Field(..., ge=0, le=50)

    num_credit_lines: int = Field(..., ge=0, le=50)

    num_delinquencies: int = Field(..., ge=0, le=20)

    debt_to_income_ratio: float = Field(..., ge=0, le=1)

    savings_balance: float = Field(..., ge=0)

class ApplicationResponse(BaseModel):
    id: UUID
    input_data: dict
    approval_score: float
    approved: bool
    risk_level: str
    recommendation: str
    created_at: datetime

    class Config:
        from_attributes = True