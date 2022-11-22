from pymongo import MongoClient
from classes_and_files import settings
from gridfs import GridFS
import os
import zlib
import pathlib
from datetime import date, timedelta

CONNECTION_STRING = settings.init()['connection_string']
clientMongo = MongoClient(CONNECTION_STRING)
mongoDB = clientMongo["TelegramDumpFinder"]
collection = mongoDB["files.metadata"]
files=mongoDB['fs.files']
fs = GridFS(mongoDB)

class Mongo:
    
    """
    Classe framework Mongo
    """

    def mongo_put(file_name):
        global file_map
        if os.path.exists('classes_and_files/temp_dir'):
            for file in os.listdir('classes_and_files/temp_dir'):
                if file_name in file:
                    file_extension = pathlib.Path('classes_and_files/temp_dir/'+file).suffix
                    metadata = {
                        "_id": file_name,
                        "file_extension": file_extension
                    }
                    collection.insert_one(metadata)
                    f = open('classes_and_files/temp_dir/'+file, "rb")
                    compressed_file = zlib.compress(f.read(), zlib.Z_BEST_COMPRESSION)
                    fs.put(compressed_file, filename=file_name)


    def mongo_get(filename):
        data = mongoDB.fs.files.find_one({'filename': filename})
        extension_dict = collection.find_one({'_id': filename})
        file_extension = extension_dict['file_extension']
        my_id= data['_id']
        outputdata=fs.get(my_id).read()
        if not os.path.exists('classes_and_files/temp_dir'):
            os.mkdir(os.path.join('classes_and_files/temp_dir'))
        output=open("classes_and_files/temp_dir/"+filename+file_extension, "wb")
        decompressed_file = zlib.decompress(outputdata)
        output.write(decompressed_file)
        output.close

    def mongo_expire():
        cursor = files.find()
        for record in cursor:
            if record['uploadDate'].date() + timedelta(weeks=1) <= date.today(): # versione corretta
            #if record['uploadDate'].date() >= date.today():                    versione di prova
                print("Dump ",record['filename']," scaduto")
                fs.delete(record['_id'])

    def exists(file_name):
        return fs.exists(filename=file_name)
