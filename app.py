from flask import Flask, request, jsonify, render_template
from groq import Groq
import sqlite3
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Database setup
conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT
    )
""")
conn.commit()

chat_history = []

def save_expense(amount, category, description):
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
        (amount, category, description, date)
    )
    conn.commit()
    return f"Saved ₹{amount} for {category} - {description}"

def get_expenses():
    cursor.execute("SELECT amount, category, description, date FROM expenses")
    rows = cursor.fetchall()
    if not rows:
        return "No expenses recorded yet."
    total = sum(row[0] for row in rows)
    result = "Your expenses:\n"
    for row in rows:
        result += f"• ₹{row[0]} on {row[1]} ({row[2]}) on {row[3]}\n"
    result += f"\nTotal: ₹{total}"
    return result

def chat(user_message):
    chat_history.append({"role": "user", "content": user_message})
    
    system_prompt = """You are a personal AI assistant that helps track expenses.
    When user mentions spending money, extract amount, category, description.
    Reply ONLY in JSON format:
    For expense: {"type": "expense", "amount": 200, "category": "food", "description": "lunch"}
    For show expenses: {"type": "show_expenses"}
    For normal chat: {"type": "chat", "reply": "your response here"}
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            *chat_history
        ]
    )
    
    reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})
    
    try:
        data = json.loads(reply)
        if data["type"] == "expense":
            result = save_expense(data["amount"], data["category"], data["description"])
            return f"Got it! {result}"
        elif data["type"] == "show_expenses":
            return get_expenses()
        else:
            return data["reply"]
    except:
        return reply

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    user_message = request.json.get("message")
    response = chat(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)