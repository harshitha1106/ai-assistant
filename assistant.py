from groq import Groq
import sqlite3
import json
from datetime import datetime

# Setup AI
client = Groq(api_key="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")

# Setup Database
conn = sqlite3.connect("expenses.db")
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

# Chat history for memory
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
        result += f"- ₹{row[0]} on {row[1]} ({row[2]}) on {row[3]}\n"
    result += f"Total: ₹{total}"
    return result

def chat(user_message):
    chat_history.append({"role": "user", "content": user_message})
    
    system_prompt = """You are a personal AI assistant that helps track expenses.
    
    When user mentions spending money, extract:
    - amount (number)
    - category (food, transport, shopping, etc.)
    - description
    
    Reply in JSON format like this when expense detected:
    {"type": "expense", "amount": 200, "category": "food", "description": "lunch"}
    
    For normal questions reply in JSON like this:
    {"type": "chat", "reply": "your response here"}
    
    For showing expenses reply:
    {"type": "show_expenses"}
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

# Main loop
print("AI Assistant ready! Type 'quit' to exit.")
print("Try: 'I spent ₹200 on food' or 'show my expenses'")
print("-" * 40)

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    response = chat(user_input)
    print(f"Assistant: {response}\n")