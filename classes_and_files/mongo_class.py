from pymongo import MongoClient
from classes_and_files import settings
from gridfs import GridFS
import os
import zlib
import pathlib
from datetime import date, timedelta, datetime

CONNECTION_STRING = settings.init()['connection_string']
clientMongo = MongoClient(CONNECTION_STRING)
mongoDB = clientMongo["TelegramDumpFinder"]
collection = mongoDB['files.metadata']
files=mongoDB['fs.files']
fs = GridFS(mongoDB)

class Mongo:
    
    """
    Classe framework Mongo
    """

    def mongo_put(file_name):
        
        """
        Metodo che inserisce all'interno del database un nuovo dump scaricato in precedenza e posizionato in una cartella temporanea
       
        :param file_name Il nome del dump collocato nella cartella e da caricare sul database
        """
        
        global file_map
        if os.path.exists('classes_and_files/temp_dir'):
            for file in os.listdir('classes_and_files/temp_dir'):
                if file_name in file:
                    file_extension = pathlib.Path('classes_and_files/temp_dir/'+file).suffix
                    metadata = {
                        "_id": file_name,
                        "file_extension": file_extension,
                        "download_date": datetime.now()
                    }
                    collection.insert_one(metadata)
                    f = open('classes_and_files/temp_dir/'+file, "rb")
                    compressed_file = zlib.compress(f.read(), zlib.Z_BEST_COMPRESSION)
                    fs.put(compressed_file, filename=file_name)


    def mongo_get(filename):
        
        """
        Metodo che recupera un dump dal database e lo salva su una cartella temporanea per effettuare operazioni di scraping
       
        :param filename Nome del dump da cercare nel database
        """
        
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
        
        """
        Metodo che rimuove dal database i dump presenti da almeno una settimana e quindi considerati non più aggiornati
        """

        cursor = collection.find()
        for record in cursor:
            if record['download_date'].date() + timedelta(weeks=1) <= date.today(): # versione corretta
            #if record['download_date'].date() <= date.today():                   # versione di prova
                print("Dump ",record['_id']," scaduto")
                collection.delete_one({'_id':record['_id']})
                file_id = fs.find_one({'filename': record['_id']})._id
                fs.delete(file_id)

    def exists(file_name):
        return fs.exists(filename=file_name)
