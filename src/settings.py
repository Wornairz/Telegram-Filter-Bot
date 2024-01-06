import yaml
from telegram.ext import Application
from telethon import TelegramClient
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection

with open("config/settings.yaml", encoding="utf-8") as yaml_config:
    config_map = yaml.safe_load(yaml_config)

TOKEN = config_map["token"]
API_ID = config_map["api_id"]
API_HASH = config_map["api_hash"]
PHONE_NUMBER = config_map["phone_number"]
# TODO: remove those three settings after create database
CHANNELS = []
KEYWORDS = []
USERS = config_map["destination_users"].split(",")
DB_URI = config_map["db_uri"]
DB_COLLECTION = config_map["db_collection"]

telegram_client = TelegramClient("bot", API_ID, API_HASH).start(phone=PHONE_NUMBER)
telegram_application = Application.builder().token(TOKEN).build()

db_collection = MongoClient(DB_URI).get_database()[DB_COLLECTION]


def get_telegram_client() -> TelegramClient:
    return telegram_client

def get_telegram_application() -> Application:
    return telegram_application

def get_db_collection() -> Collection:
    return db_collection


