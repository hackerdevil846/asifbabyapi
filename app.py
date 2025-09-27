from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="templates")

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCkgmBbGJC1UGIOmyFXesPMsqrHyZvbhqc")

def get_gemini_response(user_input):
    # Use the correct model name - gemini-pro is deprecated for this API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [
            {
                "parts": [{"text": user_input}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data and len(data['candidates']) > 0:
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                return "I apologize, but I didn't receive a proper response. Could you please try again?"
        else:
            return f"I apologize, but I'm currently unable to process your request. (Error: {response.status_code})"
    except Exception as e:
        return "I apologize, but I'm experiencing technical difficulties. Please try again later."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        user_message = request.args.get("message")
    else:
        user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response_text = get_gemini_response(user_message)
    
    return jsonify({"reply": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)