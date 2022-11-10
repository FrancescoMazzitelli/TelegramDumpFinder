import paho.mqtt.client as mqtt
import json
import threading
from classes_and_files import settings
from classes_and_files.teleLib import ToScrape


request_to_find = dict()
client = mqtt.Client(client_id="telegram")
client.connect(settings.init()["broker_address"])
telegram_lib = ToScrape

def on_message(client, userdata, message):
    """
    Callback che consente di interagire con i messaggi ricevuti;
    la stringa di bytes ricevuta dal broker mqtt viene salvata
    in una variabile come dictionary in modo da renderne agevole
    la lettura e la modifica.

    :param client: Nome del client
    :param userdata: Metadati
    :param message: Messaggio ricevuto
    """

    print("Debug message: messaggio ricevuto")
    request = json.loads(message.payload.decode("utf-8"))
    global request_to_find
    request_to_find = request

class TelegramDumpFinder:

    """
    Framework di backend principale
    """

    def __get_dump_metadata(self):
        toConvert = ToScrape.get_data_to_send(ToScrape)
        if toConvert is not None and toConvert.get("sender id") is not None:
            stringToSend = json.dumps(toConvert)
            return stringToSend

    @staticmethod
    async def __send_data(self):

        """
        Metodo privato adibito al trasferimento del risultato della ricerca
        sui gruppi telegram sul broker MQTT
        """

        stringToSend = TelegramDumpFinder.__get_dump_metadata(TelegramDumpFinder)
        if stringToSend is not None:
            client.publish(topic="Dump", payload=stringToSend)
            print("Debug message: messaggio pubblicato sul broker")

    @staticmethod
    def __listening(self):

        """
        Metodo privato che contiene il loop infinito di listening
        per la ricezione continua di messaggi
        """

        client.subscribe(topic="Request")
        client.on_message = on_message
        client.loop(10)

    @staticmethod
    async def __find_dump(self):

        """
        Metodo privato che recupera il nome del dump dalla variabile globale,
        ricerca il dump tra i gruppi e pulisce la cache
        """

        global request_to_find
        if request_to_find.get("dump_name") is not None:
            tofind = request_to_find.get("dump_name")
            if await telegram_lib.find_dump(tofind):
                print("Debug message: dump trovato")
            else:
                print("Debug message: dump non trovato")

            request_to_find.clear()

    @staticmethod
    def listening_thread(self):

        """
        Metodo che consente di istanziare un thread adibito al
        listening continuo dei messaggi che vengono pubblicati
        sul broker
        """

        listening_thread = threading.Thread(target=TelegramDumpFinder.__listening(TelegramDumpFinder), args=(1,))
        listening_thread.start()

    @staticmethod
    async def finding_thread(self):

        """
        Metodo che conesente di instanziare un thread adibito
        alla ricerca delle informazioni contenute nella variabile globale
        sui gruppi telegram
        """

        finding_thread = threading.Thread(target=await TelegramDumpFinder.__find_dump(TelegramDumpFinder), args=(1,))
        finding_thread.start()

    @staticmethod
    async def sending_thread(self):

        """
        Metodo che consente di instanziare un thread adibito
        all'inoltro delle informazioni ricercate su telegram
        al broker MQTT, appena queste sono disponibili
        """

        sending_thread = threading.Thread(target=await TelegramDumpFinder.__send_data(TelegramDumpFinder), args=(1,))
        sending_thread.start()
