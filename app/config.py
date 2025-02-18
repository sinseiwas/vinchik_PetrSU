import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
IS_DEV_SERVER = os.getenv("IS_DEV_SERVER") == "true"
PHOTO_FOLDER = os.path.abspath(os.getenv("PHOTO_FOLDER"))
DATABASE_URL = os.getenv("DATABASE_URL")
