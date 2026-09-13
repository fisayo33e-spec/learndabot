import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from content import LESSONS, QUIZZES, TIPS, WORDS

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

user_scores = {}
user_streaks = {}


def get_quiz_keyboard(quiz):
    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"quiz:{opt}:{quiz['answer']}")]
        for opt in quiz["options"]
    ]
    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_scores.setdefault(user.id, 0)
    user_streaks.setdefault(user.id, 1)

    text = (
        f"👋 Hi {user.first_name}!\n\n"
        "Welcome to *Learn Daily* — your daily dose of knowledge.\n\n"
        "Here's what I can do:\n"
        "📅 /lesson — Get a random educational lesson\n"
        "🧠 /quiz — Take a quick quiz\n"
        "💡 /tip — Get a study tip\n"
        "📖 /word — Word of the day\n"
        "📊 /progress — See your score and streak\n\n"
        "Start learning now! 🚀"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📚 *Learn Daily — Help*\n\n"
        "/start — Welcome message\n"
        "/lesson — Random educational lesson\n"
        "/quiz — Take a quiz\n"
        "/tip — Get a study tip\n"
        "/word — Word of the day\n"
        "/progress — Your score and streak\n"
        "/help — Show this menu"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(LESSONS))


async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(TIPS))


async def word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    w, meaning, example = random.choice(WORDS)
    text = f"📖 *{w}*\n\n*Meaning:* {meaning}\n\n*Example:* _{example}_"
    await update.message.reply_text(text, parse_mode="Markdown")


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quiz_data = random.choice(QUIZZES)
    await update.message.reply_text(
        f"🧠 *Quiz Time!*\n\n{quiz_data['q']}",
        reply_markup=get_quiz_keyboard(quiz_data),
        parse_mode="Markdown",
    )


async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    score = user_scores.get(user.id, 0)
    streak = user_streaks.get(user.id, 1)
    text = (
        f"📊 *Your Progress*\n\n"
        f"✅ Correct Answers: *{score}*\n"
        f"🔥 Daily Streak: *{streak} day(s)*\n\n"
        "Keep it up! 💪"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, chosen, correct = query.data.split(":", 2)
    user_id = query.from_user.id

    if chosen == correct:
        user_scores[user_id] = user_scores.get(user_id, 0) + 1
        await query.edit_message_text(
            f"✅ Correct! The answer is *{correct}*.\n\nWell done! 🎉",
            parse_mode="Markdown",
        )
    else:
        await query.edit_message_text(
            f"❌ Not quite. You chose *{chosen}*.\n"
            f"The correct answer is *{correct}*.\n\n"
            "Try another one with /quiz!",
            parse_mode="Markdown",
        )


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set!")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("lesson", lesson))
    app.add_handler(CommandHandler("tip", tip))
    app.add_handler(CommandHandler("word", word))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("progress", progress))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("LearnDailyBot is starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
