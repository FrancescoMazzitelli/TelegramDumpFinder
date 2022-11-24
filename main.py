from cheroot import wsgi
from flask import Flask, jsonify
from classes_and_files.backend import TelegramDumpFinder
from classes_and_files.mongo_class import Mongo

flask_app = Flask(__name__)

@flask_app.route("/breaches/<filename>/present", endpoint='find_dump')
async def find_dump(filename):

    """
    Endpoint Rest per verificare se un dump è presente o meno su Telegram

    :param filename: Il nome del dump da cercare passato come path param
    :return: Il messaggio di risposta sottoforma di json
    """
    
    await TelegramDumpFinder.expire_data(flask_app)
    result = await TelegramDumpFinder.find_dump(filename)
    return jsonify(result)

@flask_app.route("/breaches/<filename>/<string_to_find>", endpoint='download_dump')
async def download_dump(filename, string_to_find):

    """
    Endpoint Rest per effettuare grep su un dump presente su Telegram

    :param filename: Nome del dump da analizzare
    :param string_to_find: Filtro utilizzato per fare grep sul dump
    :return: Il messaggio di risposta sottoforma di json
    """
    
    await TelegramDumpFinder.expire_data(flask_app)
    result = await TelegramDumpFinder.download_dump(filename, string_to_find)
   
    return jsonify(result)
    

if __name__ == '__main__':

    addr = '127.0.0.1', 5000
    server = wsgi.Server(addr, flask_app)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
        print("-----------------Debug message: server stopped")
