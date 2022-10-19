"""Main entrypoint for FastAPI."""


import pickle  # noqa: S403

from fastapi import FastAPI

from iris_api.api.api_v1.api import api_v1_router
from iris_api.api.common.api import api_common_router
from iris_api.config import app_cfg
from iris_api.models.classifier import clf

from iris_api.models.iris import Iris

import pandas as pd


app = FastAPI(title="Iris ML API")


@app.on_event("startup")
async def load_model():
    """Load the model file at application startup."""
    clf.model = pickle.load(open(app_cfg.mlmodel.file, "rb"))  # noqa: S301


# app.include_router(api_v1_router, prefix="/api/v1")
app.include_router(api_common_router)


@app.post("/predict")
async def predict(iris: Iris):
    df = iris.to_dataframe()
    pred = clf.model.predict(df)
    return pred
