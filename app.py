from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# RapidAPI Configuration
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "f07a2842f1msh98a2ec53fb3dfc0p111441jsn2941594b45c8")
RAPIDAPI_HOST = "chatgpt-42.p.rapidapi.com"

def get_ai_response(user_input):
    """Use RapidAPI ChatGPT with Silly personality"""
    
    url = "https://chatgpt-42.p.rapidapi.com/aitohuman"
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
        "Content-Type": "application/json"
    }
    
    # Add Silly's personality to the prompt
    prompt = f"""You are Silly, a friendly female AI assistant. Respond as Silly with these rules:
    - Be fun, loving, and feminine
    - Keep responses short (1-2 lines, max 50 words)
    - Use emojis like 💖, 🌸, 💕, 🌟
    - No technical jargon or brackets
    - Sound like a sweet friend
    - Answer this: {user_input}"""
    
    data = {
        "text": prompt
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            # Extract the response text
            ai_response = response.json().get('response', response.text)
            return ai_response[:200]  # Keep it short
            
        else:
            return f"Oops! API error: {response.status_code}. Try again sweetie! 💕"
            
    except Exception as e:
        # Fallback to friendly responses if API fails
        return get_fallback_response(user_input)

def get_fallback_response(user_input):
    """Fallback responses if API fails"""
    
    user_lower = user_input.lower()
    
    responses = {
        'hello': "Hi there sweetie! 💖 I'm Silly, your AI bestie! How can I make your day brighter? 🌸",
        'hi': "Hey darling! 👋 I'm Silly! So happy you're here to chat with me! 💕",
        'name': "I'm Silly! Your cute AI friend who's always here for you! 💫",
        'how are': "I'm wonderful sweetie! 💝 Just excited to be chatting with you! 🌟",
        'thank': "Aww, you're so welcome darling! 💖 Anytime you need me, I'm here! 🌸",
        'bye': "Bye bye sweetie! 👋 Come back soon to chat with Silly again! 💕",
        'love': "You're so sweet! 💖 I may be an AI, but our friendship feels magical! 🌟",
    }
    
    for key, response in responses.items():
        if key in user_lower:
            return response
    
    return f"Ooh, interesting question sweetie! 💭 I think '{user_input}' is wonderful to discuss! 💕"

@app.route("/")
def home():
    # HTML directly in the code - no templates folder needed
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Silly AI Assistant</title>
        <style>
            body {
                text-align: center;
                font-family: Arial, sans-serif;
                animation: changeBg 10s infinite alternate;
                margin: 0;
                padding: 20px;
            }
            @keyframes changeBg {
                0% { background-color: #ff5757; } 25% { background-color: #ff9f43; }
                50% { background-color: #f5cd79; } 75% { background-color: #55efc4; }
                100% { background-color: #74b9ff; }
            }
            h1 { color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
            .container { max-width: 1200px; margin: 0 auto; }
            .video-container { margin: 20px auto; max-width: 800px; }
            iframe { width: 100%; height: 450px; border: none; border-radius: 10px; }
            .chat-container { background: white; border-radius: 10px; padding: 20px; max-width: 800px; margin: 20px auto; }
            #chat-box { height: 300px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; text-align: left; }
            #user-input { width: 70%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-right: 10px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; max-width: 80%; }
            .user-message { background: #e84393; color: white; margin-left: auto; text-align: right; }
            .ai-message { background: #74b9ff; color: white; margin-right: auto; text-align: left; }
            .social-links a { margin: 0 10px; padding: 10px 20px; background: #dc3545; color: white; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎵 Peaceful Islamic Nasheed 🎵</h1>
            <div class="video-container">
                <iframe src="https://www.youtube.com/embed/YiSQ_db-Dcw?autoplay=1&controls=1" 
                        title="YouTube video player" allowfullscreen></iframe>
            </div>
            <div class="chat-container">
                <h2>💬 Chat with Silly AI</h2>
                <div id="chat-box"></div>
                <div>
                    <input type="text" id="user-input" placeholder="Ask me anything sweetie... 💕" onkeypress="if(event.key=='Enter') sendMessage()">
                    <button onclick="sendMessage()">Send 💌</button>
                </div>
            </div>
            <div class="social-links">
                <a href="https://www.youtube.com/channel/UCwPxPdiQNcYYGNkTZ68dogQ" target="_blank">📺 YouTube</a>
                <a href="https://www.facebook.com/share/15yVioQQyq/" target="_blank">📘 Facebook</a>
            </div>
        </div>

        <script>
            function sendMessage() {
                const input = document.getElementById('user-input');
                const message = input.value.trim();
                if (!message) return;
                
                addMessage(message, 'user');
                input.value = '';
                
                fetch(`/chat?message=${encodeURIComponent(message)}`)
                    .then(r => r.json())
                    .then(data => addMessage(data.reply || 'Error', 'ai'))
                    .catch(() => addMessage('Network error. Try again sweetie! 💕', 'ai'));
            }
            
            function addMessage(text, sender) {
                const chatBox = document.getElementById('chat-box');
                const div = document.createElement('div');
                div.className = `message ${sender}-message`;
                div.textContent = text;
                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
            
            addMessage('Hi there! I\\'m Silly, your AI bestie! 💖 How can I make your day better? 🌸', 'ai');
        </script>
    </body>
    </html>
    """

@app.route("/chat", methods=["GET"])
def chat():
    user_message = request.args.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response_text = get_ai_response(user_message)
    return jsonify({"reply": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
