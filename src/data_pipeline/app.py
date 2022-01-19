""" Application-level logic for facilitating data pipeline """
import time
import json
from base_logger import logger
from lambda_typing.types import LambdaDict, LambdaContext

from data_extractor import DataExtractor
from db_utils import create_pymongo_client
from constants import FORMATS, NUM_TEAMS


def lambda_handler(event: LambdaDict, context: LambdaContext) -> dict:
    """Lambda handler for starting the data extraction process"""
    # format_arg = event.get("format") or ""
    format_arg = "gen8ou"
    if not format_arg:
        raise ValueError("'format' must be provided.")

    logger.info("Initializing data pipeline...")

    mongo_client = create_pymongo_client()
    data_extractor = DataExtractor(mongo_client, int(time.time()), FORMATS, NUM_TEAMS)

    # Will run successfully if errors were not raised
    _ = data_extractor.extract_info(format_arg)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "format": format_arg,
            }
        ),
    }

lambda_handler(None, None)