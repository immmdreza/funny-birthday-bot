import os

from flask import Flask


app = Flask(__name__)

env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)


@app.route("/")
def index():
    secret_key = app.config.get("SECRET_KEY")  # type: ignore
    return f"The configured secret key is {secret_key}."
