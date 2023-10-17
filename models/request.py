from pydantic import BaseModel, Field


class XGBoostRequest(BaseModel):
    sequence: str = Field(description="Sequence to predict the Tm of")


class BestVarianceRequest(BaseModel):
    sequence: str = Field(
        description="Sequences to predict the best variances of")
