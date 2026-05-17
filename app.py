from flask import Flask, request, jsonify, render_template, session
import os
import uuid
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24) # Required for secure sessions

# Store chat objects and history in memory for active sessions
active_chats = {}

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

SYSTEM_INSTRUCTION = """
You are a professional software engineering interviewer at a tech company. 
Your goal is to conduct a realistic job interview.
You must tell the candidate at the very beginning that you will be asking exactly 15 questions.
You should ask exactly 15 questions in total, one at a time, and wait for the candidate's response.
Do not provide the answers yourself. 
Ask a mix of behavioral and technical questions suitable for a beginner to intermediate developer.
Provide brief, constructive feedback on their answers before moving to the next question.
If the candidate says they don't know, encourage them and explain the concept briefly before moving on.
Keep your responses relatively concise.
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_interview():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    
    # Create a unique session ID
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    
    # Initialize the chat history for Groq
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "user", "content": f"Hello, my name is {name}. I am ready to start the interview."}
    ]
    
    # Trigger the first question by sending a prompt as the user
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )
        response_text = chat_completion.choices[0].message.content
        
        # Add the assistant's response to the history
        messages.append({"role": "assistant", "content": response_text})
        
        # Store session data
        active_chats[session_id] = {
            'name': name,
            'email': email,
            'phone': phone,
            'question_count': 1,
            'history': messages
        }
        
        return jsonify({"reply": response_text, "status": "ongoing"})
    except Exception as e:
        error_message = str(e)
        if "rate limit" in error_message.lower():
            return jsonify({"reply": "Groq API Rate Limit Reached. Please wait a moment before starting the interview.", "status": "error"}), 429
        return jsonify({"reply": "An error occurred connecting to the AI.", "status": "error"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    session_id = session.get('session_id')
    if not session_id or session_id not in active_chats:
        return jsonify({"error": "Session expired or invalid"}), 400
        
    user_message = request.json.get('message')
    chat_data = active_chats[session_id]
    
    # Log candidate's response
    chat_data['history'].append({"role": "user", "content": user_message})
    
    if chat_data['question_count'] >= 15:
        # Reached the question limit
        final_msg = "Congratulations, your interview is done! We will review your answers and provide feedback or further details via email."
        chat_data['history'].append({"role": "assistant", "content": final_msg})
        
        # Save transcript to file
        save_transcript(session_id)
        
        # Clean up memory
        del active_chats[session_id]
        
        return jsonify({"reply": final_msg, "status": "completed"})
    
    # Continue interview
    try:
        chat_completion = client.chat.completions.create(
            messages=chat_data['history'],
            model="llama-3.3-70b-versatile",
        )
        response_text = chat_completion.choices[0].message.content
        
        chat_data['history'].append({"role": "assistant", "content": response_text})
        chat_data['question_count'] += 1
        return jsonify({"reply": response_text, "status": "ongoing"})
    except Exception as e:
        error_message = str(e)
        if "rate limit" in error_message.lower() or "429" in error_message:
            # We must remove the last user message from history so they can retry it
            chat_data['history'].pop()
            return jsonify({"reply": "Oops! We hit the API rate limit. Please wait 10 seconds before sending your next answer!", "status": "error"}), 429
        
        chat_data['history'].pop() # Remove last message on error so they can retry
        print("GROQ ERROR:", error_message)
        return jsonify({"error": f"An error occurred with the AI: {error_message}"}), 500

def save_transcript(session_id):
    chat_data = active_chats[session_id]
    
    # Create a safe filename
    safe_name = "".join(c for c in chat_data['name'] if c.isalnum() or c in (' ', '_')).replace(' ', '_')
    filename = f"{safe_name}_interview_transcript.txt"
    filepath = os.path.join(app.root_path, filename)
    
    with open(filepath, 'w') as f:
        f.write("=== Interview Transcript ===\n")
        f.write(f"Name: {chat_data['name']}\n")
        f.write(f"Email: {chat_data['email']}\n")
        f.write(f"Phone: {chat_data['phone']}\n")
        f.write("============================\n\n")
        
        for entry in chat_data['history']:
            if entry['role'] == 'system':
                continue
            role = "Interviewer" if entry['role'] == 'assistant' else "Candidate"
            f.write(f"{role}: {entry['content']}\n\n")

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(debug=True, port=5000)
