from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import init_db, get_db
from models import User, Conversation, Participant, Message

app = Flask(__name__)
app.secret_key = "super_secret_key" 


init_db()

@app.route('/')
def index():
    """Shows login page."""
    if 'user_id' in session:
        return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Handles User Login/Registration."""
    username = request.form['username']
    db = get_db()
    
 
    user = db.query(User).filter_by(username=username).first()
    if not user:
        user = User(username=username, password="default_password")
        db.add(user)
        db.commit()
    
    session['user_id'] = user.id
    session['username'] = user.username
    return redirect(url_for('chat'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/chat')
def chat():
    """The Main Chat Interface."""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    db = get_db()
    current_user_id = session['user_id']
    

    users = db.query(User).filter(User.id != current_user_id).all()
    
    return render_template('chat.html', current_user=session['username'], users=users)



@app.route('/api/get_messages/<int:other_user_id>')
def get_messages(other_user_id):
    """Fetches chat history between current user and selected user."""
    db = get_db()
    my_id = session['user_id']

    my_chats = [p.conversation_id for p in db.query(Participant).filter_by(user_id=my_id).all()]
    other_chats = [p.conversation_id for p in db.query(Participant).filter_by(user_id=other_user_id).all()]
    
    common_chat_id = next((cid for cid in my_chats if cid in other_chats), None)
    
    if not common_chat_id:
        return jsonify([]) 

   
    messages = db.query(Message).filter_by(conversation_id=common_chat_id).all()
    
    data = []
    for m in messages:
        data.append({
            "sender": m.sender.username,
            "body": m.body,
            "timestamp": m.timestamp.strftime("%H:%M")
        })
    return jsonify(data)

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    receiver_id = int(data['receiver_id'])
    text = data['text']
    db = get_db()
    my_id = session['user_id']

   
    my_chats = [p.conversation_id for p in db.query(Participant).filter_by(user_id=my_id).all()]
    other_chats = [p.conversation_id for p in db.query(Participant).filter_by(user_id=receiver_id).all()]
    common_chat_id = next((cid for cid in my_chats if cid in other_chats), None)

    if not common_chat_id:
        
        new_chat = Conversation()
        db.add(new_chat)
        db.commit()
        common_chat_id = new_chat.id
        
       
        p1 = Participant(user_id=my_id, conversation_id=common_chat_id)
        p2 = Participant(user_id=receiver_id, conversation_id=common_chat_id)
        db.add_all([p1, p2])
        db.commit()

   
    msg = Message(sender_id=my_id, conversation_id=common_chat_id, body=text)
    db.add(msg)
    db.commit()

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
