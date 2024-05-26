# import openai
# import os
#
# from secret_config import API_KEY
# os.environ["OPENAI_API_KEY"] = API_KEY
# openai.api_key = os.environ["OPENAI_API_KEY"]
#
# from openai import OpenAI
# client = OpenAI()
from all_cv_text import all_text
from connectors.connection_manager import ConnectionManager
connection_manager = ConnectionManager()
open_ai = connection_manager.open_ai_connection

def create_prompt(all_text, query):
    main_prompt = [
        {
            "role": "system",
            "content": "You are a helpful assistant, help the user with any question they have about the CV presented"
        },
        {
            "role": "user",
            "content": f"This is the cv: {all_text} please answer the following question: {query}"
        }
    ]
    return main_prompt

def chat_with_gpt(query):
    prompt = create_prompt(all_text, query)
    chat_reply = open_ai.get_gpt_reply(prompt=prompt)

    return chat_reply