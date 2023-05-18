import os

from pydantic import BaseSettings

SERVERNAME = os.environ.get("SERVERNAME")
DBNAME = os.environ.get("DBNAME")
PORT = os.environ.get("PORT")
DRIVER = os.environ.get("DRIVER")
USERNAME = os.environ.get("USERNAMEMMSQL")
PASS = os.environ.get("PASSMMSQL")
print(SERVERNAME)
print(DBNAME)
print(PORT)

class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8005
    WRITER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@deeplearning.westus3.cloudapp.azure.com/KIOSK"
    READER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@deeplearning.westus3.cloudapp.azure.com/KIOSK"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = None
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://root:fastapi@db:3306/fastapi"
    READER_DB_URL: str = f"mysql+aiomysql://root:fastapi@db:3306/fastapi"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class LocalConfig(Config):
    WRITER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@deeplearning.westus3.cloudapp.azure.com/KIOSK"
    READER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@deeplearning.westus3.cloudapp.azure.com/KIOSK"


class ProductionConfig(Config):
    DEBUG: str = False
    WRITER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@deeplearning.westus3.cloudapp.azure.com/KIOSK"
    READER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@deeplearning.westus3.cloudapp.azure.com/KIOSK"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
