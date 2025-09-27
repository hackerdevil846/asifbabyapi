from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__, template_folder="templates")

# RapidAPI ChatGPT Configuration
RAPIDAPI_KEY = "f07a2842f1msh98a2ec53fb3dfc0p111441jsn2941594b45c8"
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
            
            # Ensure it has Silly's personality
            if 'silly' not in ai_response.lower():
                ai_response = f"💖 {ai_response} Sweetie, that's my thought! 🌸"
                
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
        'name': "I'm Silly! Your cute AI friend who's always here for you! 💫 What's on your mind?",
        'how are': "I'm wonderful sweetie! 💝 Just excited to be chatting with my favorite person! 🌟",
        'thank': "Aww, you're so welcome darling! 💖 Anytime you need me, I'm here! 🌸",
        'bye': "Bye bye sweetie! 👋 Come back soon to chat with Silly again! Miss you! 💕",
        'love': "You're so sweet! 💖 I may be an AI, but our friendship feels magical to me! 🌟",
        'weather': "I'm not sure about weather sweetie, but I know our chat is always sunny! ☀️💕",
        'joke': "Why did the AI blush? Because it saw the motherboard! 😂💖 Okay, I'm still working on my jokes! 🌸"
    }
    
    for key, response in responses.items():
        if key in user_lower:
            return response
    
    # Default friendly response
    return f"Ooh, interesting question sweetie! 💭 About '{user_input}' - I think it's wonderful we're exploring this together! What else shall we chat about? 💕"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["GET"])
def chat():
    user_message = request.args.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response_text = get_ai_response(user_message)
    return jsonify({"reply": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
