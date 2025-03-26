# AI-Powered Career Guidance Chatbot

An AI-driven chatbot that offers career recommendations based on user skills. This project leverages *Flask, **GPT-4 (Azure OpenAI API), and a simple **HTML/CSS frontend*.

## 🚀 Features
- AI-based career recommendations.
- Supports multiple AI models (GPT-4, DeepSeek API).
- Simple web-based UI with Flask backend.

## 🛠 Tech Stack
- *Backend*: Flask (Python)
- *AI Models*: Azure OpenAI GPT-4, DeepSeek API
- *Frontend*: HTML, CSS, JavaScript

## 📌 Setup Instructions
### ⿡ Install Dependencies
sh
pip install -r requirements.txt


### ⿢ Set Up API Keys (Environment Variables)
Update your .env file or export API keys before running:
sh
export AZURE_OPENAI_API_KEY="your_api_key"
export AZURE_ENDPOINT="your_azure_endpoint"
export DEEPSEEK_API_KEY="your_deepseek_api_key"

(For Windows, use set instead of export.)

### ⿣ Run the Flask App
sh
python app.py


### ⿤ Open the Chatbot
Visit *http://127.0.0.1:5000* in your browser.

## 🖥 Usage
1. Enter your skills in the chatbox.
2. The AI chatbot suggests careers based on your input.
3. Try different queries for varied recommendations.

## 🏆 Future Improvements
- Add multilingual support.
- Integrate real-world job market trends.
- Deploy as a web application (e.g., on AWS, Azure, or Heroku).

## 🤝 Contributing
Feel free to fork this project and enhance it!

## 📜 License
This project is licensed under the MIT License.

---
💡 *Built for Hackathons & AI Enthusiasts!* 🚀
