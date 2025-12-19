import os
from flask import Flask, jsonify, request, render_template 
from flask import Flask, jsonify, request
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the security key from the .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Configure the AI with your key
genai.configure(api_key=API_KEY)
# We use 'gemini-1.5-flash' because it's fast and free for this tier
model = genai.GenerativeModel('gemini-flash-latest')

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
# 3. Create the "Doorway" (Route)
# This allows our future website to send a message to this specific address
@app.route('/generate-survey', methods=['POST']) 
def generate_survey():
    # Get the topic from the user's request
    data = request.get_json()
    topic = data.get('topic', 'General Knowledge')

    # 4. The Prompt Strategy
    # We explicitly ask for JSON so the computer can read it easily later
    # 4. The Prompt Strategy (Updated for Options)
    prompt = f"""
    Create a survey with 20 multiple-choice questions about {topic}.
    
    Return the output as a valid JSON object with the exact key 'questions'.
    The value of 'questions' must be a list of objects, where each object has:
    - "text": The question string
    - "options": A list of 4 distinct options (strings)
    
    Example format:
    {{
      "questions": [
        {{ "text": "Question here?", "options": ["A", "B", "C", "D"] }}
      ]
    }}
    
    Do not use Markdown formatting.
    """

    response = model.generate_content(prompt)
    
    # Send the AI's text back to the website
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True)