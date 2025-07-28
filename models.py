from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True, index=True)
    time = Column(String, default="09:00")  # время рассылки

class Deck(Base):
    __tablename__ = "decks"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    user = relationship("User", back_populates="decks")

User.decks = relationship("Deck", back_populates="user")

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True)
    deck_id = Column(Integer, ForeignKey("decks.id"))
    front = Column(String)
    back = Column(String)
    ef = Column(Float, default=2.5)
    interval = Column(Integer, default=1)
    repetitions = Column(Integer, default=0)
    due = Column(DateTime, default=datetime.utcnow)
    deck = relationship("Deck", back_populates="cards")

Deck.cards = relationship("Card", back_populates="deck")
