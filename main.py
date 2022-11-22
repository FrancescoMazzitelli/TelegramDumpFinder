import asyncio
#import gunicorn
from flask import Flask, request, jsonify
from classes_and_files.backend import TelegramDumpFinder
from classes_and_files.mongo_class import Mongo
 
app = Flask(__name__)

@app.route("/breaches/<filename>/present")
async def find_dump(filename):
    result = await TelegramDumpFinder.find_dump(filename)
    return jsonify(result)

@app.route("/breaches/<filename>/<string_to_find>")
async def download_dump(filename, string_to_find):
    result = await TelegramDumpFinder.download_dump(filename, string_to_find)
    await TelegramDumpFinder.test(app)
    return jsonify(result)
    

if __name__ == '__main__':
    app.run()
