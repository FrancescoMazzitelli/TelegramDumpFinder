from telethon import TelegramClient
from pathlib import Path
from classes_and_files import settings
from tqdm import tqdm
import os

global pbar

api_id = settings.init()['api_id']
api_hash = settings.init()['api_hash']
username = settings.init()['username']
phone = settings.init()['phone']

client = TelegramClient(username, api_id, api_hash)

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

        :return: Inizializzazione della connessione e creazione del file Username.session
        """

        async with TelegramClient(username, api_id, api_hash) as client:
            await client.start()
            print("Client created")

    async def message_reader(filename):

        """
            Metodo che ritorna la lista di tutta la cronologia di messaggi inviati
            sul gruppo, il limite è stato impostato a 1000 messaggi ma è modificabile

            :param group_id: Identificatore del gruppo espresso come @nome_gruppo
            :return: Lista dei messaggi inviati
        """
        async for message in client.iter_messages(None, search=filename):
            if filename not in message.text:
                return
            entity = await client.get_entity(message.chat_id)
            if filename in message.text:
                if hasattr(entity, 'title') and hasattr(message.sender, 'username'):
                    data = {"group id": message.chat_id,
                            "group name": entity.title,
                            "sender id": message.sender_id,
                            "sender": message.sender.username,
                            "text": message.text,
                            "is message": True,
                            "date": message.date.strftime("%Y-%m-%d %H:%M:%S")}
                    return_data = data
                elif hasattr(entity, 'title'):
                    data = {"group id": message.chat_id,
                            "group name": entity.title,
                            "sender id": message.sender_id,
                            "text": message.text,
                            "is message": True,
                            "date": message.date.strftime("%Y-%m-%d %H:%M:%S")}
                    return_data = data
                else:
                    data = {"sender id": message.sender_id,
                            "sender": message.sender.username,
                            "text": message.text,
                            "is message": True,
                            "date": message.date.strftime("%Y-%m-%d %H:%M:%S")}
                    return_data = data
            return

    async def download_file(filename):

        """
        Metodo che consente di scaricare un file specifico
        e di salvarlo all'interno di una cartella temporanea

        :param filename: Nome del file da ricercare
        :return: Il file d'interesse viene scaricato nella cartella "temp"
        """

        await client.connect()
        async for message in client.iter_messages(None, search=filename):
            file = message.file
            if file is None or file.name is None:
                return
            if file is not None:
                dirToCheck = Path("classes_and_files/temp_dir")
                if not dirToCheck.exists():
                    os.mkdir(os.path.join('classes_and_files/temp_dir'))
                with DownloadProgressBar(unit='B', unit_scale=True) as t:
                    await message.download_media(file=os.path.join('classes_and_files/temp_dir/'+file.name), progress_callback=t.update_to)
                    return message.date


    async def find_dump(filename):

        """
        Metodo che recupera il riferimento ad un file dump specifico in un gruppo specifico

        :param filename: Nome del file da ricercare su telegram
        :return: Dizionario contenente i metadati del messaggio
        """

        await client.connect()
        async for message in client.iter_messages(None, search=filename):
            file = message.file
            if file is None or file.name is None:
                return
            if file is not None:
                entity = await client.get_entity(message.chat_id)
                if hasattr(entity, 'title') and hasattr(message.sender, 'username'):
                    data = {"group id": message.chat_id,
                            "group name": entity.title,
                            "sender id": message.sender_id,
                            "sender": message.sender.username,
                            "text": message.text,
                            "is message": False,
                            "date": message.date.strftime("%Y-%m-%d %H:%M:%S")}
                    
                    return data

                elif hasattr(entity, 'title'):
                    data = {"group id": message.chat_id,
                            "group name": entity.title,
                            "sender id": message.sender_id,
                            "text": message.text,
                            "is message": False,
                            "date": message.date.strftime("%Y-%m-%d %H:%M:%S")}

                    return data

                else:
                    data = {"sender id": message.sender_id,
                            "sender": message.sender.username,
                            "text": message.text,
                            "is message": False,
                            "date": message.date.strftime("%Y-%m-%d %H:%M:%S")
                            }

                    return data
            failure = {"failure message":"Non è stato trovato nessun riferimento al file desiderato su Telegram"}
            return failure

