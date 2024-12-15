import os

from bot import Config

from .tgclient import aio

if __name__ == "__main__":
    if not os.path.isdir('./bot/OUTPUTS'):
        os.makedirs('./bot/OUTPUTS')
        
    aio.run()