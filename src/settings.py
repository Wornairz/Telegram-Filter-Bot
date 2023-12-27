import yaml
from telegram.ext import Application
from telethon import TelegramClient


def build_client() -> TelegramClient:
    return TelegramClient("bot", API_ID, API_HASH).start(phone=PHONE_NUMBER)


def build_application() -> Application:
    return Application.builder().token(TOKEN).build()


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
