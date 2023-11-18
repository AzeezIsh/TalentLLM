text = open("resume_mmds/11NP1Fgf1hOP6pmX0HTbnq7GWY6eAyw4Y.pdf.mmd","r").read()
import json, os
import openai
from dotenv import load_dotenv
load_dotenv()
# openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_base = "http://0.0.0.0:8080" 

def extract(content:str):
    choice =0
    response = openai.ChatCompletion.create(
        model="test",
        messages=[{"role": "user", "content": content}],
        functions=[
            {
                "name": "infoExtract",
                "description": "extract info from resume",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "linkedin_url": {"type": "string"},
                        "portfolio_url": {"type": "string"},
                        "github_url": {"type": "string"},
                        "stackoverflow_url": {"type": "string"},
                        "name": {"type": "string"},
                        
                    }
                },
            }
        ],
        function_call="auto",

    )

    message = response["choices"][0]["message"]

    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        function_args = json.loads(message["function_call"]["arguments"])
        if function_name == "infoExtract":
            print(function_args)
            


extract(text)
