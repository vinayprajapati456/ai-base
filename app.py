import os
import json
from flask import Flask, render_template, request
from openai import AzureOpenAI  
import requests

# Initialize Flask app
app = Flask(__name__)

# Load Azure OpenAI credentials
AZURE_ENDPOINT = os.getenv("ENDPOINT_URL", "https://ai-aihackthonhub282549186415.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2025-01-01-preview")
AZURE_DEPLOYMENT = os.getenv("DEPLOYMENT_NAME", "gpt-4")
AZURE_KEY = os.getenv("AZURE_OPENAI_API_KEY", "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg")

# Load DeepSeek API credentials
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://ai-iitphackathon797339300099.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg")

# Initialize Azure OpenAI client
azure_client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_KEY,
    api_version="2024-05-01-preview",
)

def get_career_advice(user_input, model="gpt-4",language='english'):
    chat_prompt = [
        {"role": "system", "content": "You are an AI career guidance assistant. Help users with career advice based on their input."},
        {"role": "user", "content": user_input+f" Please answer in {language}."}
    ]
    
    if model == "gpt-4":
        completion = azure_client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0
        )
        return completion.choices[0].message.content
    
    elif model == "deepseek":
        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "deepseek-chat",
            "messages": chat_prompt,
            "max_tokens": 800,
            "temperature": 0.7,
            "top_p": 0.95
        }
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "Error: Unable to fetch response from DeepSeek."

@app.route("/", methods=["GET", "POST"])
def index():
    advice = ""
    model_choice = "deepseek"  # Default model
    language_choice='english'
    if request.method == "POST":
        user_input = request.form.get("user_input")
        model_choice = request.form.get("model", "azure")
        language_choice = request.form.get("language", "hindi")
        print(language_choice)
        if user_input:
            advice = get_career_advice(user_input, model_choice,language=language_choice)
    print(advice)
    return render_template("index.html", advice=advice, model_choice=model_choice,language=language_choice)

if __name__ == "__main__":
    app.run(debug=True)