from telegram import Bot, Update, Message


def process_update(bot: Bot, update: Update | None):
    if update is None:
        return

    if update.message is not None:
        _process_message(bot, update.message)

    return


def _process_message(bot: Bot, message: Message):
    if message.text:
        if message.text.startswith("/start"):
            bot.send_message(
                chat_id=message.chat_id,
                text="Hello! I'm a bot. I'm here to help you to manage your tasks.",
            )
