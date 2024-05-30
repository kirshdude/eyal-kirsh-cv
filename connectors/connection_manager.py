from connectors.secret_manager_connection import SecretManagerConnector
from connectors.open_ai_connector import OpenaiConnector
from connectors.credentials import service_account_json

OPEN_AI_MODEL = "gpt-3.5-turbo" #"gpt-4o"

class ConnectionManager:

    def __init__(self, model: str = OPEN_AI_MODEL):
        self.secret_manager_connector = SecretManagerConnector(json_key=service_account_json)
        self.openai_key = self.secret_manager_connector.get_api_key('open_ai_key')
        self.open_ai_connection = OpenaiConnector(api_key=self.openai_key, model=model)