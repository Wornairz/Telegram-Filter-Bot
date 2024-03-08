import logging
import os
from dotenv import load_dotenv
from telegram.ext import Application
from telethon import TelegramClient
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger() -> logging.Logger:
    return logging.getLogger(__name__)


load_dotenv()
TOKEN = os.getenv("TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
DB_URI = os.getenv("DB_URI")
DB_COLLECTION = os.getenv("DB_COLLECTION")

telegram_client = TelegramClient("bot", API_ID, API_HASH).start(phone=PHONE_NUMBER)
telegram_application = Application.builder().token(TOKEN).build()

db_collection = MongoClient(DB_URI).get_database()[DB_COLLECTION]


def get_telegram_client() -> TelegramClient:
    return telegram_client


def get_telegram_application() -> Application:
    return telegram_application


def get_db_collection() -> Collection:
    return db_collection
