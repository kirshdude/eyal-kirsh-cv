import openai
import os

from secret_config import API_KEY
os.environ["OPENAI_API_KEY"] = API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]

from openai import OpenAI
client = OpenAI()

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpfull assistant, help the user with any question they have about the CV presented"},
            {"role": "user", "content": f"This is the cv: {all_text} please answer the following question: {prompt}"}
        ]
    )
    return response.choices[0].message.content