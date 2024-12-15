import os
from os import getenv
from dotenv import load_dotenv

if not os.environ.get("ENV"):
    load_dotenv('.env', override=True)

class Config(object):
    TG_BOT_TOKEN = getenv("TG_BOT_TOKEN")
    APP_ID = int(getenv("APP_ID"))
    API_HASH = getenv("API_HASH")
    ADMINS = set(int(x) for x in getenv("ADMINS").split())
    BOT_USERNAME = getenv("BOT_USERNAME")

    # For pyrogram temp files
    WORK_DIR = getenv("WORK_DIR", "./bot/")
    # Just name of the Downloads Folder
    FOLDER = getenv("DOWNLOADS_FOLDER", "DOWNLOADS")
    BASE_DIR = WORK_DIR + FOLDER

    MUSIC_CHANNEL = int(getenv('MUSIC_CHANNEL'))
    PHOTO_CHANNEL = int(getenv('PHOTO_CHANNEL'))
    OUTPUT_CHANNEL = int(getenv('OUTPUT_CHANNEL'))
    CHAT = int(getenv('CHAT'))

    LOOP_AUDIO = getenv('LOOP_AUDIO')
    LOOP_VIDEO = getenv('LOOP_VIDEO')

    DATABASE_URL = getenv('DATABASE_URL')