from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__, template_folder="templates")

# DeepSeek API Configuration - Your key added directly
DEEPSEEK_API_KEY = "sk-0ed02937d6d34b9e88bb561759b02cec"

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
            return f"Oops! I'm having trouble thinking right now. (Error: {response.status_code})"
            
    except Exception as e:
        return f"Hey there! I'm currently taking a little break. Error: {str(e)}"

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
