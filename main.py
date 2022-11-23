from cheroot import wsgi
from flask import Flask, jsonify
from classes_and_files.backend import TelegramDumpFinder
from classes_and_files.mongo_class import Mongo

flask_app = Flask(__name__)

@flask_app.route("/breaches/<filename>/present", endpoint='find_dump')
async def find_dump(filename):
    result = await TelegramDumpFinder.find_dump(filename)
    return jsonify(result)

@flask_app.route("/breaches/<filename>/<string_to_find>", endpoint='download_dump')
async def download_dump(filename, string_to_find):
    result = await TelegramDumpFinder.download_dump(filename, string_to_find)
    await TelegramDumpFinder.test(flask_app)
    return jsonify(result)
    

if __name__ == '__main__':

    addr = '127.0.0.1', 5000
    server = wsgi.Server(addr, flask_app)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
        print("-----------------Debug message: server stopped")
