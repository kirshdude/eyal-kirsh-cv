import json
import os

from google.cloud import secretmanager
from google.oauth2 import service_account
from credentials import project_id


PROJECT_ID = project_id


class SecretManagerConnector:

    def __init__(self, json_key: str = None, local_env: bool = False) -> None:
        if local_env:
            credentials = json.loads(os.environ['BIG_QUERY_JSON'])
            self.credentials = service_account.Credentials.from_service_account_info(credentials)
        elif json_key is not None:
            credentials = json.loads(json_key, strict=False)
            self.credentials = service_account.Credentials.from_service_account_info(credentials)
        else:
            self.credentials = None

    def get_api_key(self, secret_key_name: str):
        client = secretmanager.SecretManagerServiceClient(credentials=self.credentials)
        secret_name = f"projects/{PROJECT_ID}/secrets/{secret_key_name}/versions/latest"
        response = client.access_secret_version(request={"name": secret_name})
        return response.payload.data.decode("UTF-8")
