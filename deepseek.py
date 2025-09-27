import requests
import os
from dotenv import load_dotenv

load_dotenv()

# DeepSeek API Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-0ed02937d6d34b9e88bb561759b02cec")

# User chat history storage
chat_histories = {}

def get_deepseek_response(user_id, user_message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    # Get user's chat history
    if user_id not in chat_histories:
        chat_histories[user_id] = []

    # Add new message to history
    chat_histories[user_id].append({"role": "user", "content": user_message})
    
    # Keep only last 5 messages
    if len(chat_histories[user_id]) > 5:
        chat_histories[user_id].pop(0)

    # Prepare messages with system prompt
    messages = [
        {
            "role": "system", 
            "content": "Your name is silly. You are a friendly AI assistant. You have knowledge about everything. Answer questions clearly and provide fun examples when needed. Don't give unnecessary information - just answer what is asked. Keep replies short (1-2 lines, max 50 words). Act like a female friend - be fun and loving. No bracket replies."
        }
    ] + chat_histories[user_id]

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post("https://api.deepseek.com/v1/chat/completions", 
                               headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data['choices'][0]['message']['content']
            
            # Store AI response in history
            chat_histories[user_id].append({"role": "assistant", "content": ai_response})
            
            return ai_response
        else:
            return f"Oops! I'm having trouble thinking right now. (Error: {response.status_code})"
            
    except Exception as e:
        return f"Hey there! I'm currently taking a little break. Error: {str(e)}"
