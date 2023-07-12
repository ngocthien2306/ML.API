import os

from pydantic import BaseSettings

SERVERNAME = os.environ.get("SERVERNAME")
DBNAME = os.environ.get("DBNAME")
PORT = os.environ.get("PORT")
DRIVER = os.environ.get("DRIVER")
USERNAME = os.environ.get("USERNAMEMMSQL")
PASS = os.environ.get("PASSMMSQL")
IMAGE_NOT_FOUND_PATH = './public/images/image_not_available.png'

class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
<<<<<<< HEAD

    APP_HOST: str = "26.115.12.45"
    APP_PORT: int = 8005
    WRITER_DB_URL: str = "mssql+pyodbc:///?odbc_connect=" \
        "Driver={SQL Server};Server=A301-09\\PARKINGSITE;" \
        "Database=KIOSK;Uid=parkingai;Pwd=thien123;"
    READER_DB_URL: str = "mssql+pyodbc:///?odbc_connect=" \
        "Driver={SQL Server};Server=A301-09\\PARKINGSITE;" \
        "Database=KIOSK;Uid=parkingai;Pwd=thien123;"
=======
    APP_HOST: str = "127.0.0.1"

    APP_PORT: int = 8001
    WRITER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@26.236.244.191/KIOSK"
    READER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@26.236.244.191/KIOSK"

>>>>>>> 09843b8649b955c906365652917bcc776f2d6f09
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
<<<<<<< HEAD
    WRITER_DB_URL: str = "mssql+pyodbc:///?odbc_connect=" \
        "Driver={SQL Server};Server=A301-09\\PARKINGSITE;" \
        "Database=KIOSK;Uid=parkingai;Pwd=thien123;"
    READER_DB_URL: str = "mssql+pyodbc:///?odbc_connect=" \
        "Driver={SQL Server};Server=A301-09\\PARKINGSITE;" \
        "Database=KIOSK;Uid=parkingai;Pwd=thien123;"
=======
    WRITER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@26.236.244.191/KIOSK"
    READER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@26.236.244.191/KIOSK"
>>>>>>> 09843b8649b955c906365652917bcc776f2d6f09


class ProductionConfig(Config):
    DEBUG: str = False
<<<<<<< HEAD

    WRITER_DB_URL: str = "mssql+pyodbc:///?odbc_connect=" \
        "Driver={SQL Server};Server=A301-09\\PARKINGSITE;" \
        "Database=KIOSK;Uid=parkingai;Pwd=thien123;"
    READER_DB_URL: str = "mssql+pyodbc:///?odbc_connect=" \
        "Driver={SQL Server};Server=A301-09\\PARKINGSITE;" \
        "Database=KIOSK;Uid=parkingai;Pwd=thien123;"
=======
    WRITER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@26.236.244.191/KIOSK"
    READER_DB_URL: str = f"mssql+pymssql://deeplearning:thien123@26.236.244.191/KIOSK"
>>>>>>> 09843b8649b955c906365652917bcc776f2d6f09


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
