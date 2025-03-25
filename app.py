import os
import json
from flask import Flask, render_template, request, session, jsonify
from openai import AzureOpenAI
import requests
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Load Azure OpenAI credentials
AZURE_ENDPOINT = os.getenv("ENDPOINT_URL", "https://ai-aihackthonhub282549186415.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2025-01-01-preview")
AZURE_DEPLOYMENT = os.getenv("DEPLOYMENT_NAME", "gpt-4")
AZURE_KEY = os.getenv("AZURE_OPENAI_API_KEY", "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg")

# Load DeepSeek API credentials
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://ai-iitphackathon797339300099.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg")

if not AZURE_KEY or not DEEPSEEK_API_KEY:
    raise ValueError("API keys are missing. Set them as environment variables.")

# Initialize Azure OpenAI client
azure_client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_KEY,
    api_version="2024-05-01-preview",
)

def get_career_advice(user_input, model="gpt-4", language='english'):
    chat_prompt = [
        {"role": "system", "content": "You are an AI career guidance assistant. Help users with career advice based on their input."},
        {"role": "user", "content": user_input + f" Please answer in {language}."},
    ]

    if model == "gpt-4":
        try:
            completion = azure_client.chat.completions.create(
                model=AZURE_DEPLOYMENT,
                messages=chat_prompt,
                max_tokens=800,
                temperature=0.7,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0
            )
            return {"role": "gpt-4", "content": completion.choices[0].message.content}
        except Exception as e:
            print(f"Error calling GPT-4: {e}")
            return {"role": "error", "content": "Sorry, I encountered an error while processing your request with GPT-4."}

    elif model == "deepseek":
        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "deepseek-chat",
            "messages": chat_prompt,
            "max_tokens": 800,
            "temperature": 0.7,
            "top_p": 0.95
        }
        try:
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes
            return {"role": "deepseek", "content": response.json()["choices"][0]["message"]["content"]}
        except requests.exceptions.RequestException as e:
            print(f"Error calling DeepSeek API: {e}")
            return {"role": "error", "content": "Sorry, I encountered an error while processing your request with DeepSeek."}
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing DeepSeek response: {e}")
            return {"role": "error", "content": "Sorry, I received an unexpected response from DeepSeek."}

@app.route("/", methods=["GET", "POST"])
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []
    model_choice = request.args.get('model', 'gpt-4')  # Get model from query params and set default to gpt-4
    language_choice = request.args.get('language', 'english') # Get language from query params

    if request.method == "POST":
        user_input = request.form.get("user_input")
        model_choice = request.form.get("model", "gpt-4")  # Set default model to gpt-4
        language_choice = request.form.get("language", "english")

        if user_input:
            session['chat_history'].append({"role": "user", "content": user_input})
            response = get_career_advice(user_input, model=model_choice, language=language_choice)
            session['chat_history'].append(response)
            session.modified = True  # To ensure the session is saved

    return render_template("index.html", chat_history=session['chat_history'], model_choice=model_choice, language=language_choice)

@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    session.pop('chat_history', None)
    return jsonify({"message": "Chat history cleared"})

@app.route("/get_chat_history", methods=["GET"])
def get_chat_history():
    return jsonify(session.get('chat_history', []))

if __name__ == "__main__":
    app.run(debug=True)