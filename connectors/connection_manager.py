from connectors.secret_manager_connection import SecretManagerConnector
from connectors.open_ai_connector import OpenaiConnector
from connectors.credentials import service_account_json

class ConnectionManager:

    def __init__(self):
        self.secret_manager_connector = SecretManagerConnector(json_key=service_account_json)
        self.openai_key = self.secret_manager_connector.get_api_key('open_ai_key')
        self.open_ai_connection = OpenaiConnector(api_key=self.openai_key)