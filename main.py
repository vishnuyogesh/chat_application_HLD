# main.py
from database import init_db, get_db
from models import User, Conversation, Participant, Message

def create_user(session, username, password):
    """Registers a new user."""
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        print(f"User '{username}' already exists.")
        return existing_user
    
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    print(f"User '{username}' created!")
    return new_user

def create_conversation(session, user1_id, user2_id):
    """Creates a chat room between two users."""
    
    chat = Conversation()
    session.add(chat)
    session.commit() 

    
    p1 = Participant(user_id=user1_id, conversation_id=chat.id)
    p2 = Participant(user_id=user2_id, conversation_id=chat.id)
    session.add_all([p1, p2])
    session.commit()
    
    print(f"Chat started between User {user1_id} and User {user2_id} (Chat ID: {chat.id})")
    return chat

def send_message(session, sender_id, chat_id, text):
    """Sends a message in a specific chat."""
    msg = Message(sender_id=sender_id, conversation_id=chat_id, body=text)
    session.add(msg)
    session.commit()
    print(f"Message sent: '{text}'")

def get_chat_history(session, chat_id):
    """Fetches and displays messages for a chat."""
    chat = session.query(Conversation).get(chat_id)
    if not chat:
        print("Chat not found.")
        return

    print(f"\n--- History for Chat {chat_id} ---")
    for msg in chat.messages:
        sender_name = msg.sender.username
        print(f"[{msg.timestamp.strftime('%H:%M')}] {sender_name}: {msg.body}")
    print("---------------------------------\n")

if __name__ == "__main__":
    
    init_db()
    db = get_db()


    print("\n--- Creating Users ---")
    alice = create_user(db, "Alice", "password123")
    bob = create_user(db, "Bob", "securepass")
    charlie = create_user(db, "Charlie", "12345")

 
    print("\n--- Starting Conversation ---")
    chat_ab = create_conversation(db, alice.id, bob.id)

    
    print("\n--- Sending Messages ---")
    send_message(db, alice.id, chat_ab.id, "Hey Bob! How is the project going?")
    send_message(db, bob.id, chat_ab.id, "Hey Alice. It's going well, thanks!")
    send_message(db, alice.id, chat_ab.id, "Great. Let's meet at 5pm.")

    get_chat_history(db, chat_ab.id)

    chat_bc = create_conversation(db, bob.id, charlie.id)
    send_message(db, bob.id, chat_bc.id, "Charlie, are you coming?")
    get_chat_history(db, chat_bc.id)