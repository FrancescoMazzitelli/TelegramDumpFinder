import shutil

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from pathlib import Path
from tqdm import tqdm
import json, datetime, os


def date_format(date):
    """
    :param message:
    :return:
    """
    if type(date) is datetime:
        return date.strftime("%Y-%m-%d %H:%M:%S")


class ToScrape:
    """
    Framework Telegram per DarkWeb Monitor
    """

    global client, settings, api_id, api_hash, username, phone

    fileJ = open('settings.json')
    settings = json.load(fileJ)
    api_id = settings['api_id']
    api_hash = settings['api_hash']
    username = settings['username']
    phone = settings['phone']

    async def init(self):
        """
        Metodo che inizializza il client Telegram effettuando l'operazione
        di login con l'autenticazione a due fattori

        :return: Inizializzazione della connessione
        """
        async with TelegramClient(username, api_id, api_hash) as client:
            await client.start()

            print("Client created")
            await client.disconnect()

    async def message_reader(group_id):
        """
            Questo metodo ritorna la lista di tutta la cronologia di messaggi inviati
            sul gruppo, il limite è stato impostato a 1000 messaggi ma è modificabile

            :param group_id: Identificatore del gruppo espresso come @nome_gruppo
            :return: Lista dei messaggi inviati
        """
        mex_list = []

        async with TelegramClient(username, api_id, api_hash) as client:
            messages = await client.get_messages(group_id, limit=1000)
            for message in messages:
                if not message.sender_id is None and not message.sender.username is None:
                    data = {"group": group_id,
                            "sender id": message.sender_id,
                            "sender": message.sender.username,
                            "text": message.text,
                            "date": message.date.strftime("%Y-%m-%d %H:%M:%S")}
                    if not data.get("text") is None:
                        mex_list.append(data)
            client.disconnect()
            return mex_list

    def print_mex_list(mex_list):
        """
            Metodo che stampa a schermo il contenuto della lista statica
            adibita allo storage dei messaggi

            :param mex_list: Lista di messaggi da stampare a schermo
        """
        for i in range(0, len(mex_list)):
            print(mex_list[i])

    async def download_file(group_id, filename):
        """
        Metodo che consente di scaricare un file specifico da un gruppo
        e di salvarlo all'interno di una cartella temporanea

        :param group_id: Identificatore del gruppo espresso come @nome_gruppo
        :param filename: Nome del file da ricercare nel gruppo
        :return: Il file d'interesse viene scaricato nella cartella "temp"
        """
        async with TelegramClient(username, api_id, api_hash) as client:
            messages = await client.get_messages(group_id, limit=1000)
            for msg in tqdm(messages):
                file = msg.file
                if not file is None and not file.name is None and filename in file.name:
                    dirToCheck = Path("temp_dir")
                    if not dirToCheck.exists():
                        os.mkdir(os.path.join('temp_dir'))
                    await msg.download_media(file=os.path.join('temp_dir/'+file.name))

    async def find_dump(group_id, filename):
        """
        Metodo che recupera il riferimento ad un file dump specifico in un gruppo specifico

        :param group_id: Identificatore del gruppo espresso come @nome_gruppo
        :param filename: Nome del file da ricercare nel gruppo
        :return: File json contenente i metadati del messaggio
        """
        async with TelegramClient(username, api_id, api_hash) as client:
            messages = await client.get_messages(group_id, limit=1000)
            for msg in messages:
                file = msg.file
                if not file is None and not file.name is None and filename in file.name:
                    data = {"group": group_id,
                            "sender id": msg.sender_id,
                            "sender":msg.sender.username,
                            "text": msg.text,
                            "date": msg.date.strftime("%Y-%m-%d %H:%M:%S")}
                    #Scrivo l'oggetto json sul file dump.json
                    dirToCheck = Path("dump_dir")
                    if not dirToCheck.exists():
                        os.mkdir(os.path.join('dump_dir'))
                    with open("dump_dir/file_location.json", "w+") as outfile:
                        json.dump(data, outfile)

    def clear_cache(dir_name):
        """
        Metodo che elimina i file salvati temporaneamente, da usare dopo aver inviato
        i dati tramite MQTT

        :param dir_name: Nome della directory da eliminare
        :return: Eliminazione della directory contenente i file temporanei scaricati
        """
        shutil.rmtree(dir_name)