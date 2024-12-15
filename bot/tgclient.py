from config import Config

from pyrogram import Client

plugins = dict(
    root="bot/modules"
)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "Buuutt",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.TG_BOT_TOKEN,
            plugins=plugins,
            workdir=Config.WORK_DIR,
            workers=100
        )

    async def start(self):
        await super().start()
        print("Bot Started.....")

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped.....")

aio = Bot()