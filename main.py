import asyncio, os, json, time, threading
from pathlib import Path
from classes_and_files.teleLib import ToScrape
from classes_and_files.backend import TelegramDumpFinder

test = TelegramDumpFinder

async def backend_test():
    test.listening_thread(test)
    await test.finding_thread("@salvatorebevilacqua")

if __name__ == '__main__':
    #asyncio.run(main_test())
    #send_data("test.mosquitto.org")
    asyncio.run(backend_test())