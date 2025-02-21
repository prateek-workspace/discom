import google.generativeai as genai
from django.conf import settings

# Configure the API
genai.configure(api_key=settings.GEMINI_API_KEY)

def get_ai_response(message_text):
    try:
        # Use the gemini-pro model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate response
        response = model.generate_content(
            f"As a helpful assistant in a discussion forum, respond to: {message_text}"
        )
        
        return response.text
    except Exception as e:
        return f"Error generating AI response: {str(e)}" 