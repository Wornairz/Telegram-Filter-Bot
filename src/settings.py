import yaml
from telegram.ext import Application
from telethon import TelegramClient

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

client = TelegramClient("bot", API_ID, API_HASH).start(phone=PHONE_NUMBER)
application = Application.builder().token(TOKEN).build()


def get_client() -> TelegramClient:
    return client


def get_application() -> Application:
    return application
