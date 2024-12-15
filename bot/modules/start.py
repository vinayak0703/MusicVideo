import os
import asyncio

from bot import CMD
from config import Config
from pyrogram import Client, filters
from pyrogram.types import Message

from ..helpers.pg_impl import musictable, phototable
from ..helpers.ffmpeg import create_video

@Client.on_message(filters.command(CMD.START))
async def start(c:Client, msg:Message):
    if msg.from_user.id not in Config.ADMINS:
        return

    while True:
        try:
            await init_video(c, msg)
            await init_video(c, msg)

            await c.send_message(msg.chat.id, 'Sleeping for 12hr')
            await asyncio.sleep(12*60*60)
        except Exception as e:
            await c.send_message(
                Config.CHAT,
                str(e)
            )
            await asyncio.sleep(1*60*60)


async def init_video(c, msg):

    item_id, title, msg_id = musictable.get_random()

    if not msg_id:
        return await c.send_message(
            Config.CHAT,
            'Failed to fetch music from channel\nCancelling cron job.....'
        )

    msg = await c.get_messages(
        Config.MUSIC_CHANNEL,
        msg_id
    )
        
    music_path = await c.download_media(
        msg
    )

    msg_id = phototable.get_random()

    msg = await c.get_messages(
        Config.PHOTO_CHANNEL,
        msg_id
    )

    if not msg:
        return await c.send_message(
            Config.CHAT,
            'Failed to fetch thumbnail from channel\nCancelling cron job.....'
        )

    photo_path = await c.download_media(
        msg
    )

    output = await create_video(photo_path, music_path, Config.LOOP_VIDEO, Config.LOOP_AUDIO)

    if os.path.isfile(output):
        await c.send_video(
            Config.OUTPUT_CHANNEL,
            output
        )
        musictable.drop_item(item_id)
        os.remove(output)

    try:
        os.remove(photo_path)
        os.remove(music_path)
    except:
        pass


    await c.send_message(
        chat_id=int(Config.CHAT),
        text='Sucessfully created Music Video'
    )


@Client.on_message(filters.audio)
async def set_music(c:Client, msg:Message):
    if msg.chat.id == int(Config.MUSIC_CHANNEL):
        title = msg.audio.file_name
        msg_id = msg.id

        musictable.set_variable(title, msg_id)


@Client.on_message(filters.document)
async def set_doc(c:Client, msg:Message):
    if msg.chat.id == int(Config.PHOTO_CHANNEL):
        msg_id = msg.id
        phototable.set_variable(msg_id)

@Client.on_message(filters.animation or filters.video)
async def set_video(c:Client, msg:Message):
    if msg.chat.id == int(Config.PHOTO_CHANNEL):
        msg_id = msg.id
        phototable.set_variable(msg_id)



@Client.on_message(filters.command(CMD.DROP_PHOTO))
async def drop_photo(c:Client, msg:Message):
    phototable.drop_table()
    print('dropped photo')

@Client.on_message(filters.command(CMD.DROP_MUSIC))
async def DROP_MUSIC(c:Client, msg:Message):
    musictable.drop_table()
    print('dropped audio')