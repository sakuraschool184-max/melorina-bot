user_history = {}

def add_user_message(user_id, text):
    if user_id not in user_history:
        user_history[user_id] = []
    user_history[user_id].append(f"User: {text}")

def add_bot_message(user_id, text):
    if user_id not in user_history:
        user_history[user_id] = []
    user_history[user_id].append(f"Bot: {text}")

def get_history(user_id):
    return "\n".join(user_history.get(user_id, []))
