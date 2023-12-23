import yaml

with open("config/settings.yaml") as yaml_config:
    config_map = yaml.safe_load(yaml_config)

TOKEN = config_map["token"]
API_ID = config_map["api_id"]
API_HASH = config_map["api_hash"]
PHONE_NUMBER = config_map["phone_number"]

CHANNELS = config_map["channels"].split(",")
KEYWORDS = config_map["keywords"].split(",")
