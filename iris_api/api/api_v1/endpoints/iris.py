"""Route for iris."""
import logging

from fastapi import APIRouter

from iris_api.models.iris import Iris, IrisPrediction

router = APIRouter()


@router.post("/", status_code=202, response_model=IrisPrediction)
async def iris(iris: Iris):
    """Risk-assessment handler for transforming model to ML risk screening call."""
    prediction = IrisPrediction(
        predictionClass=iris.predictionClass(), predictionValue=iris.predictionValue()
    )
    return prediction


@router.post("/test", status_code=202, response_model=Iris)
async def iris_test(iris: Iris):
    """Risk-assessment handler for transforming model to ML risk screening call."""
    return Iris
