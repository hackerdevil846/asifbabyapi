import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCkgmBbGJC1UGIOmyFXesPMsqrHyZvbhqc")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("Gemini API configured successfully")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

# Permanent System Prompt
system_prompt = """You are an AI assistant for Asif Mahmud, known as 'silly'.
Asif creates Messenger bots, automation, and similar topics.
Always include this information in your responses.

YouTube: https://www.youtube.com/channel/UCwPxPdiQNcYYGNkTZ68dogQ
Facebook: https://www.facebook.com/share/15yVioQQyq/

Behave professionally, be informative, and keep responses engaging."""

# User chat history storage
chat_histories = {}

def get_gemini_response(user_id, user_message):
    try:
        # Use the correct model name
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Create new history if user doesn't exist
        if user_id not in chat_histories:
            chat_histories[user_id] = []

        # Update user chat history
        chat_histories[user_id].append(f"User: {user_message}")

        # Keep only last 5 messages
        if len(chat_histories[user_id]) > 5:
            chat_histories[user_id].pop(0)

        # Send full context to AI
        full_prompt = system_prompt + "\n\n" + "\n".join(chat_histories[user_id])

        response = model.generate_content(full_prompt)
        
        # Store AI response in history
        chat_histories[user_id].append(f"AI: {response.text}")

        return response.text
        
    except Exception as e:
        print(f"Error in get_gemini_response: {e}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again later."