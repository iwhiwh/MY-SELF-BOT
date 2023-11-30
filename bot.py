import logging
import logging.config
import sys
import glob
import importlib
import asyncio

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from pathlib import Path
from pyrogram import idle
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from Script import script 
from datetime import date, datetime 
from aiohttp import web
from plugins import web_server
import pytz

from jkdevloper import Lusi_Films_Bot
from util.keepalive import ping_server
from jkdevloper.clients import initialize_clients

ppath = "plugins/*.py"
files = glob.glob(ppath)
Lusi_Films_Bot.start()
loop = asyncio.get_event_loop()

async def lusifilms_start():
    print('\n')
    print('Initalizing Lusifilms Bot')
    bot_info = await Lusi_Films_Bot.get_me()
    Lusi_Films_Bot.username = bot_info.username
    await initialize_clients()
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("LusiFilms Started => " + plugin_name)
    if ON_HEROKU:
        asyncio.create_task(ping_server())
    b_users, b_chats = await db.get_banned()
    temp.BANNED_USERS = b_users
    temp.BANNED_CHATS = b_chats
    await super().start()
    await Media.ensure_indexes()
    me = await Lusi_Films_Bot.get_me()
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    Lusi_Films_Bot.username = '@' + me.username
    logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
    logging.info(LOG_STR)
    logging.info(script.LOGO)
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    app = web.AppRunner(await web_server()) 
    await app.setup() 
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    time = now.strftime("%H:%M:%S %p")
    await Lusi_Films_Bot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    await idle()


if __name__ == '__main__':
    try:
        loop.run_until_complete(lusifilms_start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')



    
