from dotenv import load_dotenv
import os

load_dotenv()

BOT_TG = os.getenv("BOT_TG")
VENICE = os.getenv("VENICE")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")