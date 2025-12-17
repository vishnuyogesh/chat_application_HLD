from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)

    
    messages = relationship("Message", back_populates="sender")
    participants = relationship("Participant", back_populates="user")

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    last_message_at = Column(DateTime, default=datetime.utcnow)

   
    messages = relationship("Message", back_populates="conversation")
    participants = relationship("Participant", back_populates="conversation")

class Participant(Base):
    __tablename__ = 'participants'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    
    user = relationship("User", back_populates="participants")
    conversation = relationship("Conversation", back_populates="participants")

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    body = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    sender_id = Column(Integer, ForeignKey('users.id'))
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    
    sender = relationship("User", back_populates="messages")
    conversation = relationship("Conversation", back_populates="messages")