from pydantic import BaseModel, Field


class XGBoostResponse(BaseModel):
    tm: float = Field(description="Predicted Tm")


class BestVarianceResponse(BaseModel):
    sequences: list = Field(
        description="List of sequences to predict the Tm of")
    tms: list = Field(description="List of predicted Tms")
