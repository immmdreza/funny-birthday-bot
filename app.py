import os
import re

from flask import Flask, request
from telegram import Bot, Message
from telegram.update import Update

from update_managers.update_manager import UpdateManager
from my_filters.message_filters import TextRegex


app = Flask(__name__)

env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)


bot_token: str = app.config.get("BOT_TOKEN")  # type: ignore
if not bot_token:
    raise ValueError("BOT_TOKEN is not set")

bot = Bot(bot_token)
manager = UpdateManager(bot)


base_url: str = app.config.get("BASE_URL")  # type: ignore
if not base_url:
    raise ValueError("BASE_URL is not set")


me = bot.get_me()
print(f"Hello! My name is {me.first_name}")

try:
    if bot.set_webhook(url=f"{base_url}/updates/{bot_token}"):
        print("Webhook setup success")
except Exception:
    print("Webhook setup failed")


@app.route("/")
def index():
    return f"This is from {env_config} version."


@app.post(f"/updates/{bot_token}")
def updates():
    manager.enqueue_update(Update.de_json(request.get_json(), bot))
    return {"ok": True}


@manager.register_message(TextRegex(re.compile("^/start", re.IGNORECASE)))
def echo(bot: Bot, message: Message) -> None:
    if message.text is not None:
        message.reply_text(
            "Hello! Here is the @FunnyBirthdayBot 🎂.\n"
            "While i'm with you, you'll never forget a birthday again."
            "\n\nJust let me join your group."
        )
