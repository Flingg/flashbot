import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters)
from database import SessionLocal, engine
from models import Base, User, Deck, Card
from datetime import datetime
from scheduler import review
from telegram.ext.jobqueue import JobQueue

Base.metadata.create_all(bind=engine)
logging.basicConfig(level=logging.INFO)

session = SessionLocal()

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = session.query(User).filter_by(chat_id=uid).first()
    if not user:
        user = User(chat_id=uid)
        session.add(user)
        session.commit()
    keyboard = [[InlineKeyboardButton("Add", callback_data="add"),
                 InlineKeyboardButton("List", callback_data="list")],
                [InlineKeyboardButton("Set time", callback_data="settime"),
                 InlineKeyboardButton("Progress", callback_data="progress")]]
    await ctx.bot.send_message(chat_id=uid,
        text="Welcome! Choose:", reply_markup=InlineKeyboardMarkup(keyboard))

# handlers for /add, /list, /settime, inline flows – omitted for brevity

async def send_due_cards(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.utcnow()
    for user in session.query(User).all():
        for deck in user.decks:
            for card in deck.cards:
                if card.due <= now:
                    await context.bot.send_message(chat_id=user.chat_id, text=card.front)
                    # save context of expecting answer...
                    # schedule sending back, waiting for user grade...
