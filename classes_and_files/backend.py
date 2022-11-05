import paho.mqtt.client as mqtt
import teleLib, asyncio

connection_flag = 0

async def main_test():
    test = teleLib.ToScrape
    #await test.init(test)
    #mex_list = await test.message_reader('@salvatorebevilacqua')
    #test.print_mex_list(mex_list)
    #await test.download_file('@salvatorebevilacqua', 'ToDo_list')
    #await test.find_dump('@salvatorebevilacqua', 'ToDo_list')
    #test.clear_cache('temp_dir')

def on_connect():
   global connection_flag
   connection_flag = 1

def on_disconnect():
   global connection_flag
   connection_flag = 0

def connect(broker_address):
    client = mqtt.Client("P1")
    client.on_connect = on_connect()
    client.on_disconnect = on_disconnect()
    client.connect("test.mosquitto.org")
    client.publish("Dumps - 39900532", "Hello")
    print(connection_flag)



if __name__ == '__main__':
    #asyncio.run(main_test())
    connect("test.mosquitto.org")
