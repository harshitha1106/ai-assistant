# AI Assistant with Expense Tracking

A production-style Python project that combines a conversational AI assistant with automatic expense detection, SQLite storage, and secure API key handling.

## Overview

This project simulates a personal AI assistant that can chat naturally while also acting as a lightweight expense tracker.  
It detects expense-related messages, stores them in a local SQLite database, and uses conversation memory to respond with better context over time.

## Key Features

- Natural language chatbot conversations
- Automatic detection of expense-related inputs
- Persistent storage using SQLite database
- Conversation memory (context-aware responses)
- Secure API key management via `.env` file (no hard-coded secrets)
- Clean, minimal codebase suitable for beginners and reviewers

## Tech Stack

- **Language:** Python  
- **Database:** SQLite  
- **APIs:** OpenAI / LLM-based API (configurable)  
- **Environment Management:** `python-dotenv`  
- **Version Control:** Git & GitHub  

## Architecture

- `app.py` – main application logic and conversation loop  
- `database.db` – SQLite database for storing expenses  
- `models/` (if present) – helpers for database or message handling  
- `.env` – stores API keys and secrets (excluded from Git)  
- `requirements.txt` – Python dependencies  

```bash
ai-assistant/
│── app.py
│── database.db
│── requirements.txt
│── .env            # not committed to Git
│── README.md
└── (any helper modules)
```

## How It Works

1. The user sends a message to the assistant.
2. The assistant generates a natural reply using the configured AI model.
3. The app checks if the message contains expense-related information (amounts, categories, etc.).
4. If yes, the expense is parsed and stored in the SQLite database.
5. Previous conversation history is used to maintain context and improve responses.

## Setup & Installation

1. **Clone the repository**

```bash
git clone https://github.com/harshitha1106/ai-assistant.git
cd ai-assistant
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:

```env
API_KEY=your_api_key_here
```

5. **Run the application**

```bash
python app.py
```

## Example Use Cases

- Log daily expenses through natural conversation  
- Build a starting point for a personal finance assistant  
- Learn how to combine AI APIs with a local database  
- Practice secure secret handling in real projects  

## What I Learned

Working on this project helped me practice:

- Structuring a small but realistic Python application  
- Integrating an AI/LLM API into a backend  
- Using SQLite for simple persistent storage  
- Handling environment variables securely with `.env`  
- Writing cleaner, more readable code for open source and portfolios  

## Author

**Harshitha**  
- GitHub: [@harshitha1106](https://github.com/harshitha1106)
- Role: 2nd-year Electronics & Communication Engineering student exploring AI and web development
