import paho.mqtt.client as mqtt
from pathlib import Path
import asyncio, os, json, time, threading
from classes_and_files.teleLib import ToScrape

fileJ = open('classes_and_files/settings.json')
settings = json.load(fileJ)
broker_address = settings['broker_address']

client = mqtt.Client(client_id="telegram")
client.connect(broker_address)
telegram_lib = ToScrape

def on_message(client, userdata, message):
    """
    Callback che consente di interagire con i messaggi ricevuti;
    la stringa di bytes ricevuta dal broker mqtt viene salvata
    su un file .json. Questa operazione consente di convertire agevolmente
    bytes in oggetti json

    :param client: Nome del client
    :param userdata: Metadati
    :param message: Messaggio ricevuto
    :return: Creazione di un file request.json
    """
    request = message.payload.decode("utf-8")
    print("Debug message: messaggio ricevuto")
    dirToCheck = Path("classes_and_files/request_dir")
    if not dirToCheck.exists():
        os.mkdir(os.path.join('classes_and_files/request_dir'))
    request_json = open("classes_and_files/request_dir/request.json", "w")
    request_json.write(request)


class TelegramDumpFinder():
    """
    Framework di backend principale
    """

    def find_local_data(pathTo):
        """
        Metodo che ricerca e crea oggetti json con riferimento a
        files sul filesystem

        :param pathTo: Percorso del file desiderato
        :return: Oggetto json
        """
        with open(pathTo, 'r') as file:
            json_read = json.load(file)
            return json_read

    def find_local_data_conversion(pathTo):
        """
        Metodo che ricerca e crea oggetti json con riferimento a
        files sul filesystem e li converte in stringhe per facilitarne
        l'inoltro sul broker MQTT

        :param pathTo: Percorso del file desiderato
        :return: Oggetto json convertito in stringa
        """
        with open(pathTo, 'r') as file:
            json_read = json.load(file)
            json_object = json.dumps(json_read)
            return json_object

    async def __send_data(self):
        """
        Metodo privato adibito al trasferimento del risultato della ricerca
        sui gruppi telegram sul broker MQTT

        :return:
        """
        #while True:
        dirToCheck = Path("classes_and_files/dump_dir")
        pathTo = "classes_and_files/dump_dir/file_location.json"
        if dirToCheck.exists() and os.path.exists(pathTo):
            client.publish(topic="Dump", payload=TelegramDumpFinder.find_local_data_conversion(pathTo))
            print("Debug message: messaggio pubblicato sul broker")
            telegram_lib.clear_cache("classes_and_files/dump_dir")


    def __listening(self):
        """
        Metodo privato che contiene il loop infinito di listening
        per la ricezione continua di messaggi
        """
        client.subscribe(topic="Request")
        client.on_message = on_message
        client.loop(10)

    async def __find_dump(group_id):
        """
        Metodo privato che acquisisce il nome del dump dal file json, pulisce
        la cache e ricerca il file nel gruppo

        :param group_id: Identificativo del gruppo all'interno del quale effettuare la ricerca
        :return:
        """
        #while True:
        dirToCheck = Path("classes_and_files/request_dir")
        pathTo = "classes_and_files/request_dir/request.json"
        if dirToCheck.exists() and os.path.exists(pathTo):
            data = TelegramDumpFinder.find_local_data(pathTo)
            tofind = data.get("dump_name")
            telegram_lib.clear_cache("classes_and_files/request_dir")
            await telegram_lib.find_dump(group_id, tofind)

            dirToCheck = Path("classes_and_files/dump_dir")
            if dirToCheck.exists():
                print("Debug message: dump trovato")

    def listening_thread(self):
        """
        Metodo che consente di istanziare un thread adibito al
        listening continuo dei messaggi che vengono pubblicati
        sul broker
        """
        listening_thread = threading.Thread(target=TelegramDumpFinder.__listening(TelegramDumpFinder), args=(1,))
        listening_thread.start()

    async def finding_thread(group_id):
        """
        Metodo che conesente di instanziare un thread adibito
        alla ricerca delle informazioni contenute nel file ricevuto
        dal broker MQTT sui gruppi telegram

        :param group_id: Gruppi telegram su cui cercare
        """
        finding_thread = threading.Thread(target= await TelegramDumpFinder.__find_dump(group_id), args=(1,))
        finding_thread.start()

    async def sending_thread(self):
        """
        Metodo che consente di instanziare un thread adibito
        all'inoltro delle informazioni ricercate su telegram
        al broker MQTT, appena queste sono disponibili
        """
        sending_thread = threading.Thread(target= await TelegramDumpFinder.__send_data(TelegramDumpFinder), args=(1,))
        sending_thread.start()


#+----------------------------------------------------------------------------------------------------------------------TEST


if __name__ == '__main__':
    #asyncio.run(main_test())
    #send_data("test.mosquitto.org")
    asyncio.run(backend_test())

async def teleLib_test():
    print("Hello")
    #test = teleLib.ToScrape
    #await test.init(test)
    #mex_list = await test.message_reader('@salvatorebevilacqua')
    #test.print_mex_list(mex_list)
    #await test.download_file('@salvatorebevilacqua', 'ToDo_list')
    #await test.find_dump('@salvatorebevilacqua', 'ToDo_list')
    #test.clear_cache('temp_dir')

async def backend_test():
    test = TelegramDumpFinder
    test.listening_thread(test)
    dirToCheck = Path("classes_and_files/request_dir")
    if dirToCheck.exists():
        await test.find_dump("@salvatorebevilacqua")
