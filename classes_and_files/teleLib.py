from telethon import TelegramClient
from pathlib import Path
from classes_and_files import settings
from tqdm import tqdm
import os

api_id = settings.init()['api_id']
api_hash = settings.init()['api_hash']
username = settings.init()['username']
phone = settings.init()['phone']

class DownloadProgressBar(tqdm):
    def update_to(self, current, total):
        self.total = total
        self.update(current - self.n)

class ToScrape:

    """
    Framework Telegram per DarkWeb Monitor
    """

    @staticmethod
    async def init(self):

        """
        Metodo che inizializza il client Telegram effettuando l'operazione
        di login con l'autenticazione a due fattori

        :return: Inizializzazione della connessione e creazione del file di sessione
        """

        async with TelegramClient(username, api_id, api_hash) as client:
            await client.start()
            print("Client creato")


    @staticmethod
    async def download_file(filename):

        """
        Metodo che consente di scaricare un file specifico e di salvarlo all'interno di una cartella temporanea

        :param filename: Nome del file da ricercare
        :return: Il file d'interesse viene scaricato nella cartella temporanea
        """
        
        async with TelegramClient(username, api_id, api_hash) as client:
            await client.connect()
            async for message in client.iter_messages(None, search=filename):
                file = message.file
                if file is not None and file.name is not None:
                    dirToCheck = Path("classes_and_files/temp_dir")
                    if not dirToCheck.exists():
                        os.mkdir(os.path.join('classes_and_files/temp_dir'))
                    with DownloadProgressBar(unit='B', unit_scale=True) as t:
                        await message.download_media(file=os.path.join('classes_and_files/temp_dir/'+file.name), progress_callback=t.update_to)
                        await client.disconnect()
                        return message.date
            return

    @staticmethod
    async def find_dump(filename):

        """
        Metodo che recupera il riferimento ad un file dump specifico in un gruppo specifico

        :param filename: Nome del file da ricercare su telegram
        :return: Dizionario contenente i metadati del file
        """

        async with TelegramClient(username, api_id, api_hash) as client:
            await client.connect()
            data = dict()
            flag = False
            messages = await ToScrape.__iter_messages(client, filename)
            for message in messages:
                file = message.file
                if file is not None and hasattr(file, 'name'):
                    entity = await client.get_entity(message.chat_id)
                    data = await ToScrape.__data_package(client, entity, message, flag)
                    break
            if data == dict():
                return
            client.disconnect()
            return data

    @staticmethod
    async def message_reader(filename):
        
        """
        Metodo che ricerca un messaggio all'interno di tutte le chat di Telegram,
        in riferimento al file d'interesse

        :param filename: Nome del file da ricercare 
        :return: Dizionario contenente i metadati del file
        """

        async with TelegramClient(username, api_id, api_hash) as client:
            await client.connect()
            data = dict()
            flag = True
            messages = await ToScrape.__iter_messages(client, filename)
            for message in messages:
                file = message.file
                if file is None:
                    entity = await client.get_entity(message.chat_id)
                    data = await ToScrape.__data_package(client, entity, message, flag)
                    break
            if data == dict():
                return
            await client.disconnect()
            return data

    async def __data_package(client, entity, message, flag):
        """
        Metodo privato utilizzato per strutturare i metadati estratti e creare
        un dizionario per una successiva generazione di un file json da spedire

        :param client: client da terminare
        :param entity: entità dal quale estrarre il nome del gruppo/canale
        :param message: entità dal quale vengono estratti i metadati
        :return: dati da spedire
        """
        if hasattr(entity, 'title') and hasattr(message.sender, 'username'):
                    data = {"group id": message.chat_id,
                            "group name": entity.title,
                            "sender id": message.sender_id,
                            "sender": message.sender.username,
                            "text": message.text,
                            "is message": flag,
                            "date": message.date.strftime("%Y-%m-%d %H:%M:%S"),
                            "exist": True
                            }

                    await client.disconnect()
                    return data

        elif hasattr(entity, 'title'):
            data = {"group id": message.chat_id,
                    "group name": entity.title,
                    "sender id": message.sender_id,
                    "text": message.text,
                    "is message": flag,
                    "date": message.date.strftime("%Y-%m-%d %H:%M:%S"),
                    "exist": True
                    }

            await client.disconnect()
            return data

        else:
            data = {"sender id": message.sender_id,
                    "sender": message.sender.username,
                    "text": message.text,
                    "is message": flag,
                    "date": message.date.strftime("%Y-%m-%d %H:%M:%S"),
                    "exist": True
                    }

            await client.disconnect()
            return data

    async def __iter_messages(client, filename):
        """
        Metodo privato che si occupa di salvare i messaggi trovati sul client
        Telegram in una lista temporanea

        :param client: client sul quale ricercare i messaggi
        :param filename: nome del file/contenuto del messaggio da ricercare
        :return: lista di messaggi
        """
        await client.connect()
        messages = list()
        async for mex in client.iter_messages(None, search=filename, limit=10):
            if not mex in messages:
                messages.append(mex)
        return messages