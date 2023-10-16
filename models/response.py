from pydantic import BaseModel, Field


class XGBoostResponse(BaseModel):
    tm: float = Field(description="Predicted Tm")