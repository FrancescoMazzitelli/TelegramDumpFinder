import asyncio
from classes_and_files.backend import TelegramDumpFinder
from classes_and_files.teleLib import ToScrape

app = TelegramDumpFinder()
client = ToScrape()

async def run():
    while True:
        app.listening_thread(app)
        await app.finding_thread(app)
        await app.sending_thread(app)

if __name__ == '__main__':
    asyncio.run(run())
