import os


class Config:
    DEBUG = False
    DEVELOPMENT = False
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    BASE_URL = os.getenv("BASE_URL", "")


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
