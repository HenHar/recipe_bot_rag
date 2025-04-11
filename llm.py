import base64
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class Prompts:
    recipe_prompt = """
    Helfe dem Nutzer bei Fragen zum Thema Kochen, Rezepte, Einkaufslisten und Küche. Antworte auf Deutsch. Gebe auch eine URL zum Rezept mit an. Ignoriere, wenn der User ein Foto erwähnt. Verwende, wenn vorhanden, folgende Rezepte:
    {}
    User: {}
    """

    describe_image_prompt = """
    Beschreibe was auf dem Foto zu sehen ist. Liste alle enthaltene Zutaten auf.
    """






"""
#openai_api_base = "http://localhost:8000/v1"
OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")
#base_url = "https://openrouter.ai/api/v1"
#model_version = "meta-llama/llama-3.1-8b-instruct:free"

runpod_api_key =  os.getenv("RUNPOD_API_KEY")

model_version = "VAGOsolutions/Llama-3.1-SauerkrautLM-8b-Instruct"
runpod_endpoint_id="qs5d7ya3791y56"

model_version = "meta-llama/Llama-3.1-8B-Instruct"
runpod_endpoint_id="5xxl1ezib4zli6"

base_url = f"https://api.runpod.ai/v2/{runpod_endpoint_id}/openai/v1"

client = OpenAI(
    api_key=runpod_api_key,
    base_url=base_url
)
"""


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
model_version = "gpt-4o-mini"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_response(image_path, prompt):
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content