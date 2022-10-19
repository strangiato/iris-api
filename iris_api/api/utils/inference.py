"""Utilities for handling inferences."""

import json
import logging

from kafka import KafkaProducer

import requests

from iris_api.config import app_cfg
from iris_api.models.risk_assessment import RiskAssessment
from iris_api.models.risk_predictor import RiskPredictor, InferenceResult


def inference_task(risk_assessment: RiskAssessment):
    """Task for processing risk_assessment posts."""
    logging.info("Starting inferce task")
    ml_result = risk_prediction(risk_assessment)
    write_message(ml_result.json())


def write_message(
    message: str,
    kafka_bootstrap: str = app_cfg.kafka.bootstrap,
    topic: str = app_cfg.kafka.topic_out,
):
    """Write ml inference results back to kafka."""
    logging.info("Writing message to kafka")
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap)
    producer.send(topic=topic, value=message.encode("utf-8"))


def risk_prediction(risk_assessment: RiskAssessment) -> InferenceResult:
    """Perform ml_inference and map the results back to a risk_prediction."""
    # {"data":{"names":["t:0"],"ndarray":[[0.1, 0.2]]},"meta":{"requestPath":{"classifier":"image-registry.openshift-image-registry.svc:5000/risk-assessment/risk-assessment-ml-service:latest"}}}
    inference_response = json.loads(ml_inference(risk_assessment))

    logging.debug(inference_response)

    self_harm_codes = RiskPredictor(
        oneWeek=inference_response["data"]["ndarray"][0][0],
        twoWeeks=inference_response["data"]["ndarray"][0][1],
        threeWeeks=inference_response["data"]["ndarray"][0][2],
        oneMonth=inference_response["data"]["ndarray"][0][3],
    )

    self_harm_survey = RiskPredictor(
        oneWeek=inference_response["data"]["ndarray"][0][4],
        twoWeeks=inference_response["data"]["ndarray"][0][5],
        threeWeeks=inference_response["data"]["ndarray"][0][6],
        oneMonth=inference_response["data"]["ndarray"][0][7],
    )

    ideation = RiskPredictor(
        oneWeek=inference_response["data"]["ndarray"][0][8],
        twoWeeks=inference_response["data"]["ndarray"][0][9],
        threeWeeks=inference_response["data"]["ndarray"][0][10],
        oneMonth=inference_response["data"]["ndarray"][0][11],
    )

    inference_result = InferenceResult(
        patientId=risk_assessment.patientId,
        selfHarmCodes=self_harm_codes,
        selfHarmSurvey=self_harm_survey,
        ideation=ideation,
    )
    return inference_result


def ml_inference(risk_assessment: RiskAssessment, url=app_cfg.mlservice.host) -> str:
    """POST risk_assessment object to MLService and return a response."""
    predict_url = f"{url}/api/v1.0/predictions"
    headers = {"Content-Type": "application/json"}

    columns = risk_assessment.columns_list()
    X = risk_assessment.values_list()

    logging.debug("columns = {columns}")
    logging.debug("X = {X}")

    data_obj = json.dumps({"data": {"names": columns, "ndarray": X}})

    try:
        r = requests.post(predict_url, headers=headers, data=data_obj)
        r.raise_for_status
    except requests.exceptions.ConnectionError:
        logging.exception("Unable to connect to the MLService.")
        raise
    except requests.exceptions.Timeout:
        logging.exception("The request to the MLService timed out.")
        raise
    except requests.exceptions.HTTPError:
        logging.exception("An HTTP error occured.")
        raise
    except requests.exceptions.RequestException:
        logging.exception("An unknown error occured")

    return r.text
