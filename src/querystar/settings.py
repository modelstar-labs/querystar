import os
from dataclasses import dataclass, field
from dotenv import load_dotenv


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


settings = QuerystarSettings()