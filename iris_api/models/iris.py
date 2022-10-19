"""Iris object classes."""
from typing import Union

from fastapi.encoders import jsonable_encoder

import pandas as pd

import pickle

from pydantic import BaseModel


class Iris(BaseModel):
    """Iris model for ml prediction."""

    sepalLength: float
    sepalWidth: float
    petalLength: float
    petalWideth: float

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(jsonable_encoder(self), index=[0])
        return df

    # def predictionClass(self) -> int:
    #     df = self.to_dataframe()
    #     prediction =
    #     return 1

    # def predictionValue(self) -> str:
    #     return "iris_type"


class IrisPrediction(BaseModel):
    """Iris prediction model for response."""

    predictionClass: Union[int, None] = None
    predictionValue: Union[str, None] = None
