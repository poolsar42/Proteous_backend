from pydantic import BaseModel, Field


class XGBoostRequest(BaseModel):
    sequence: str = Field(description="Sequence to predict the Tm of")