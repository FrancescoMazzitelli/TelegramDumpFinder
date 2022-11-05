import paho.mqtt.client as mqtt
from pathlib import Path
import teleLib, asyncio, os, json, time, threading

fileJ = open('settings.json')
settings = json.load(fileJ)
broker_address = settings['broker_address']

client = mqtt.Client(client_id="telegram")
test = teleLib.ToScrape


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
    dirToCheck = Path("request_dir")
    if not dirToCheck.exists():
        os.mkdir(os.path.join('request_dir'))
    request_json = open("request_dir/request.json", "w")
    request_json.write(request)


class TelegramDumpFinder:
    """
    Framework principale
    """

    def find_local_data(path):
        with open(pathTo, 'r') as file:
            json_read = json.load(file)
            json_object = json.dumps(json_read)
            return json_object

    def send_data(self):
        client.connect(broker_address)
        pathTo = "dump_dir/file_location.json"
        client.publish(topic="Dump", payload=find_local_data(pathTo))
        test.clear_cache("dump_dir")
        client.disconnect()

    def __listening(self):
        """
        Metodo privato che contiene il loop infinito di listening
        """
        client.connect(broker_address)
        client.subscribe(topic="Request")
        client.on_message = on_message
        client.loop_forever()

    def listening_thread(self):
        """
        Metodo che consente di istanziare un thread adibito al
        listening continuo dei messaggi che vengono pubblicati
        sul broker
        """
        thread = threading.Thread(target=test.__listening, args=(1,))
        thread.start()

    def find_dump(self):
        """

        :return:
        """

if __name__ == '__main__':
    # asyncio.run(main_test())
    #send_data("test.mosquitto.org")
    test = TelegramDumpFinder
    test.listening_thread(test)

async def teleLib_test():
    print("Hello")
    #test = teleLib.ToScrape
    #await test.init(test)
    #mex_list = await test.message_reader('@salvatorebevilacqua')
    #test.print_mex_list(mex_list)
    #await test.download_file('@salvatorebevilacqua', 'ToDo_list')
    #await test.find_dump('@salvatorebevilacqua', 'ToDo_list')
    #test.clear_cache('temp_dir')
