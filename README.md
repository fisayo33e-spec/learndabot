# LearnDailyBot 📚

A free educational Telegram bot that delivers daily lessons, quizzes, tips, and vocabulary words — no API keys required.

## ✨ Features

- 📅 `/lesson` — Random educational lesson
- 🧠 `/quiz` — Multiple-choice quiz with instant feedback
- 💡 `/tip` — Study tip
- 📖 `/word` — Word of the day
- 📊 `/progress` — Track your score
- ❓ `/help` — Show all commands

## 🚀 Deploy on Railway

1. Fork or clone this repo.
2. Go to [railway.app](https://railway.app) and sign in with GitHub.
3. Click **New Project → Deploy from GitHub repo**.
4. Select this repo. Railway auto-detects `requirements.txt`.
5. In the **Variables** tab, add:
   - `TELEGRAM_BOT_TOKEN` = your token from [@BotFather](https://t.me/BotFather)
6. Railway will deploy automatically. Check **Deployments → Logs**.

## 🖥️ Run Locally

    git clone https://github.com/YOUR_USERNAME/learn-daily-bot.git
    cd learn-daily-bot
    pip install -r requirements.txt
    export TELEGRAM_BOT_TOKEN="your_token_here"
    python bot.py

## 🔒 Security

Never commit your `.env` file or bot token. Always use environment variables.

## 📜 License

MIT — free to use, modify, and share.
