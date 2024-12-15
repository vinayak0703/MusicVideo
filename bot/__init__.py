from config import Config

bot = Config.BOT_USERNAME

class CMD(object):
    START = ["start", f"start@{bot}"]
    DROP_PHOTO = ['drop_photo', f'drop_photo@{bot}]']
    DROP_MUSIC = ['drop_music', f'drop_music@{bot}]']

cmd = CMD()