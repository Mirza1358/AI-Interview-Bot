# 🤖 AI Interview Chatbot

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black.svg?logo=flask)
![Groq](https://img.shields.io/badge/AI-Groq%20LLaMA%203-orange.svg)
![HTML5](https://img.shields.io/badge/Frontend-Glassmorphism-purple.svg)

A professional, interactive, web-based Artificial Intelligence interview platform. This application acts as an automated software engineering interviewer that evaluates candidates through a dynamic 15-question process, complete with a beautiful, modern "Glassmorphism" UI.

**🌍 Live Demo:** [http://mirza14.pythonanywhere.com/](http://mirza14.pythonanywhere.com/)

## ✨ Features

- **Automated Interview Workflow:** The AI asks exactly 15 tailored software engineering questions (mixing behavioral and technical).
- **Intelligent Feedback:** Uses the lightning-fast **Groq API (LLaMA 3 70B)** to provide constructive, real-time feedback on candidate answers.
- **Modern User Interface:** A gorgeous dark-mode frontend featuring frosted glass elements, floating background animations, and custom scrollbars.
- **Smart Validation:** Secure candidate onboarding screen with strict input validations (e.g., numeric-only phone fields).
- **Automated Data Export:** Once the interview concludes, the server automatically generates and saves a `.txt` file containing the candidate's name, email, phone, and full transcript for administrative review!
- **Rate Limit Handling:** Built-in safeguards to gracefully handle API rate limits and session expiration.

## 🛠️ Technology Stack

- **Backend:** Python, Flask, Groq API
- **Frontend:** Vanilla HTML5, CSS3, JavaScript (No heavy frameworks required!)
- **AI Model:** LLaMA-3.3-70B-Versatile (via Groq)
- **Deployment:** PythonAnywhere

## 🚀 Getting Started (Local Development)

### 1. Clone the repository
```bash
git clone https://github.com/Mirza1358/AI-Interview-Bot.git
cd AI-Interview-Bot
```

### 2. Install dependencies
Ensure you have Python 3 installed. Then run:
```bash
pip install -r requirements.txt
```

### 3. Add your API Key
Create a `.env` file in the root directory of the project and add your Groq API key:
```env
GROQ_API_KEY=gsk_your_api_key_here
```
*(You can get a free API key at [console.groq.com](https://console.groq.com/keys))*

### 4. Run the Server
```bash
python app.py
```

### 5. Access the Platform
Open your web browser and navigate to:
**http://127.0.0.1:5000**

## ☁️ Deployment (PythonAnywhere)
This project is officially hosted on PythonAnywhere. If you wish to host your own version:
1. Clone the repo in your PythonAnywhere Bash Console.
2. Run `pip3.10 install --user -r requirements.txt`.
3. Create the `.env` file in your root project directory via the PythonAnywhere file manager.
4. Set up the `_wsgi.py` file to point to your repository and `app.py`.

## 📂 Project Structure
- `app.py` - Core Flask server, routing, and Groq API logic.
- `templates/index.html` - The HTML structure of the application.
- `static/style.css` - Custom glassmorphism styling and animations.
- `static/script.js` - Dynamic DOM manipulation, API fetching, and error handling.
- `requirements.txt` - Python package dependencies.

---
*Created by [Bilal Mirza](https://github.com/Mirza1358)*
