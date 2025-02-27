import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
IS_DEV_SERVER = os.getenv("IS_DEV_SERVER") == "true"
PHOTO_FOLDER = os.path.abspath(os.getenv("PHOTO_FOLDER"))

DB_ENGINE = os.environ.get("DB_ENGINE")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_IP = os.environ.get("DB_IP")

DATABASE_URL = f"{DB_ENGINE}://{DB_USER}:{DB_PASS}@{DB_IP}:{DB_PORT}/{DB_NAME}"
