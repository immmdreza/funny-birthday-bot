import os

from flask import Flask, request
from telegram import Bot
from telegram.update import Update


app = Flask(__name__)

env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)


bot_token: str = app.config.get("BOT_TOKEN")  # type: ignore
if not bot_token:
    raise ValueError("BOT_TOKEN is not set")

bot = Bot(bot_token)

base_url: str = app.config.get("BASE_URL")  # type: ignore
if not base_url:
    raise ValueError("BASE_URL is not set")

bot.set_webhook(f"{base_url}/updates/{bot_token}")


@app.route("/")
def index():
    return f"This is from {env_config} version."


@app.post(f"/updates/{bot_token}")
def updates():
    update_json = request.get_json()
    update = Update.de_json(update_json, bot)

    if update is None:
        return

    if update.message is not None:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=update.message.text,
        )
