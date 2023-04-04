import boto3
import json
from lambda_typing.types import LambdaDict, LambdaContext
from clients.teams_ddb_client import TeamsDdbClient
from modules.ddb_teams_reader import DdbTeamsReader
from utils.base_logger import logger


TABLE_NAME = "PsIngestionTeamsTable-Beta"
GET_OPERATION = "GET"
GET_HEALTH_RESOURCE = "/health"
GET_TEAM_RESOURCE = "/teams/{team_id}"
TEAM_ID_PARAM = "team_id"


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """
    Lambda handler entrypoint
    :returns: success
    """
    logger.info(
        "Received {operation} request for {endpoint}".format(
            operation=event["httpMethod"], endpoint=event["path"]
        )
    )

    ddb_client = boto3.client("dynamodb")
    teams_ddb_client = TeamsDdbClient(ddb_client, TABLE_NAME)
    ddb_teams_reader = DdbTeamsReader(teams_ddb_client)
    res_body = {}

    if (
        event["httpMethod"] == GET_OPERATION
        and event["resource"] == GET_HEALTH_RESOURCE
    ):
        res_body = ddb_teams_reader.get_health_check()
    elif (
        event["httpMethod"] == GET_OPERATION and event["resource"] == GET_TEAM_RESOURCE
    ):
        team_id = event["pathParameters"][TEAM_ID_PARAM]
        res_body = ddb_teams_reader.get_team_by_id(team_id)
    else:
        logger.warning("Route and HTTP method do not match...")

    return build_response(res_body)


def build_response(res_body: dict):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(res_body),
    }
