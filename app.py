from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="templates")

# DeepSeek API Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def get_deepseek_response(user_input):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system", 
                "content": "Your name is silly. You are a friendly AI assistant. You have knowledge about everything. Answer questions clearly and provide fun examples when needed. Don't give unnecessary information - just answer what is asked. Keep replies short (1-2 lines, max 50 words). Act like a female friend - be fun and loving. No bracket replies."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        "stream": False
    }

    try:
        response = requests.post("https://api.deepseek.com/v1/chat/completions", 
                               headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return "Oops! I'm having trouble thinking right now. Try again sweetie! 💕"
            
    except Exception as e:
        return "Hey there! I'm currently taking a little break. Can you try again in a moment? 💕"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["GET"])
def chat():
    user_message = request.args.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response_text = get_deepseek_response(user_message)
    return jsonify({"reply": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
