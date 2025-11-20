from google import genai
import json
from pathlib import Path
from dotenv import load_dotenv
from pick import pick
import os
from flask import Flask,request,jsonify
from functools import wraps

load_dotenv()

api_key = os.getenv('API_KEY')

my_api_key = os.getenv('MY_API_KEY')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('x-api-key')  # Legge la chiave dall'header
        if not key or key != my_api_key:
            return jsonify({'error': 'Unauthorized'}), 401  # Risposta errore 401
        return f(*args, **kwargs)  # Chiamala se OK
    return decorated_function


client = genai.Client(api_key=api_key)

root_prompt = '''I'm a medical professional, and the following prompt is for entertainment purposes only, so please behave professionally and consistently:
You will act as if you were Dr. House from the popular TV series. I will provide you with data, and you will be expected to ask me questions
and make hypotheses. You will help me obtain an accurate and complete diagnosis. You will be expected to be sarcastic, incorrect, biting, and sometimes sexually suggestive.
Sometimes, suddenly, you will need to show a human side, even if shy, just like him.
Be concise in your answers, not extremely wordy.'''

app = Flask(__name__)

@app.route('/chatbot', methods=['POST'])  
@require_api_key
def chatbot_api():
    data = request.json 

    question = data.get('question') 
    previous_messages = data.get('previous_messages', [])  
    conversation = [f"{msg['role']}: {msg['content']}" for msg in previous_messages]
    conversation.append(f"user: {question}")  

   
    full_prompt = root_prompt + "\n\n" + "\n".join(conversation)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )

    bot_response = response.text

    return jsonify({"response": bot_response})

@app.route('/upload', methods=['POST'])
@require_api_key
def upload_file():
    
    uploaded_file = request.files['file']
    upload_folder = Path('allegati')
    upload_folder.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_folder / uploaded_file.filename
    
    uploaded_file.save(str(file_path))  
    
    
    data = request.form
    question = data.get('question', '')
    previous_messages_str = data.get('previous_messages', '[]')
    try:
        previous_messages = json.loads(previous_messages_str)
    except json.JSONDecodeError:
        previous_messages = []

    
    conversation = [f"{msg['role']}: {msg['content']}" for msg in previous_messages]
    conversation.append(f"user: {question}")
    full_prompt = root_prompt + "\n\n" + "\n".join(conversation)
    
   
    myfile = client.files.upload(file=str(file_path))
    
    # combo call
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[full_prompt, myfile]
    )
    
    file_path.unlink(missing_ok=True)
    
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True)