import asyncio
from classes_and_files.teleLib import ToScrape

client = ToScrape()

async def telegramClient():
    await client.init(client)

if __name__ == '__main__':
    asyncio.run(telegramClient())
