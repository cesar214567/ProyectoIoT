import os
from pathlib import Path
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent.parent

config = dotenv_values(BASE_DIR / ".env")

SENDGRID_API_KEY = config["SENDGRID_API_KEY"]
BROKER = config["BROKER"]
PORT = int(config["PORT"])
USERNAME = config["USERNAME"] if "USERNAME" in config else None
PASSWORD = config["PASSWORD"] if "PASSWORD" in config else None