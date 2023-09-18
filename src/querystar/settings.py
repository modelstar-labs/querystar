import os
import logging
from dataclasses import dataclass, field
from dotenv import load_dotenv
from querystar.logger import LoggerFormatter


def get_qs_token():
    # First, try to get the token from the environment variables
    querystar_token_envvar = os.environ.get("QUERYSTAR_TOKEN")

    if querystar_token_envvar:
        return querystar_token_envvar

    # If not found in environment variables, try to load from a .env file
    load_dotenv(".env")
    querystar_token_dotenv = os.getenv("QUERYSTAR_TOKEN")

    if querystar_token_dotenv:
        return querystar_token_dotenv

    raise Exception(
        "No `QUERYSTAR_TOKEN` found in environment variables or .env file")


@dataclass
class QuerystarSettings():
    ssl: bool = True
    querystar_server_host: str = 'dev-v1.test.server-xauto.api.querystar.io'
    querystar_token: str = field(init=False)

    def __post_init__(self):
        self.querystar_token = get_qs_token()

        # Initialize and configure the logger
        logger = logging.getLogger("querystar")
        logger.setLevel(logging.INFO)
        # logger.setLevel(logging.DEBUG)

        # Create a console handler with colored output
        console_handler = logging.StreamHandler()
        logger.addHandler(console_handler)
        console_handler.setFormatter(LoggerFormatter())


settings = QuerystarSettings()
