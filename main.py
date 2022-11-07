import asyncio, os, json, time, threading
from pathlib import Path
from classes_and_files.teleLib import ToScrape
from classes_and_files.backend import TelegramDumpFinder

app = TelegramDumpFinder

async def run():
    while True:
        app.listening_thread(app)
        await app.finding_thread("@salvatorebevilacqua")
        await app.sending_thread(app)

if __name__ == '__main__':
    asyncio.run(run())