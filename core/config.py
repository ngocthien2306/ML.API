import os
from dotenv import load_dotenv
from pydantic import BaseSettings
from urllib.parse import quote_plus

load_dotenv()

server = os.getenv("SERVER")
database = os.getenv("DATABASE")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")


# Quote the special characters in the server name and password
quoted_server = quote_plus(server)
quoted_password = quote_plus(password)

IMAGE_NOT_FOUND_PATH = './public/images/image_not_available.png'

WRITER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@deeplearning.westus3.cloudapp.azure.com/KIOSK"
READER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@deeplearning.westus3.cloudapp.azure.com/KIOSK"

connection_string_write = f"mssql+pymssql://parkingai:thien123@26.115.12.45/KIOSK"
connection_string_read = f"mssql+pymssql://parkingai:thien123@26.115.12.45/KIOSK"


print(connection_string_read)
print(connection_string_write)
class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True

    APP_HOST: str = "26.115.12.45"
    APP_PORT: int = 8005
    WRITER_DB_URL: str = connection_string_write
    READER_DB_URL: str = connection_string_read
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
    WRITER_DB_URL: str = connection_string_write
    READER_DB_URL: str = connection_string_read

class ProductionConfig(Config):
    DEBUG: str = False
    WRITER_DB_URL: str = connection_string_write
    READER_DB_URL: str = connection_string_read


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
