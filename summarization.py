import openai
import os
from dotenv import load_dotenv

load_dotenv() 

openai.api_key = os.getenv('API_KEY')

def summarize_text(text):
    print(text)
    prompt = (f"Por favor, realiza un resumen en español a detalle del siguiente texto:\n"
              f"{text}\n"
              f"Resumen:")
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.9,
        max_tokens=1000,
        n=1,
        stop=None,
        timeout=30,
    )
    summary = response.choices[0].text.strip()
    return summary