from classes_and_files.teleLib import ToScrape
from classes_and_files.mongo_class import Mongo
import os
import re
import shutil
import asyncio

telegram_lib = ToScrape

class TelegramDumpFinder:

    @staticmethod
    async def find_dump(filename):

        """
        
        """

        if filename is not None:
            to_send = await telegram_lib.find_dump(filename)
            print("-----------------Debug message: dump trovato")
            return to_send
              

    @staticmethod
    async def download_dump(filename, to_search):
        
        """
        Metodo che effettua l'operazione di grep su un file di interesse. \n
        I possibili casi d'uso del metodo sono: \n
        1) Sul filesystem esiste una cartella con all'interno i file da greppare \n
        2) Il file d'interesse non esiste ne su Mongo ne sul file system 
        viene quindi scaricato da telegram, pushato su Mongo per elaborazioni
        future e inifine greppato \n
        3) il file d'interesse esiste su Mongo, viene quindi recuperato e greppato

        :param filename: Nome del file da cercare sia localmente che su telegram a seconda dei casi
        :param to_search: Stringa da trovare nel file d'interesse per grep
        :return: Dict che verrà poi spedito tramite HTTP
        """

        dict = {"Results": []}
        if filename is not None:
            if os.path.exists('classes_and_files/temp_dir'):
                print("-----------------Debug message: dump presente sul filesystem")
                for file in os.listdir('classes_and_files/temp_dir'):
                    if filename in file:
                        f = open('classes_and_files/temp_dir/'+file, "r")
                        for line in f:
                            if re.search(to_search, line, re.IGNORECASE):
                                dict["Results"].append(line)
                        f.close()
                        TelegramDumpFinder.__clear_cache()
                        return dict

            elif not Mongo.exists(filename) and not os.path.exists('classes_and_files/temp_dir'):
                print("-----------------Debug message: dump non presente ne su Mongo ne sul filesystem")
                print("-----------------Debug message: dump in download")
                date = await telegram_lib.download_file(filename)
                Mongo.mongo_put(filename)
                for file in os.listdir('classes_and_files/temp_dir'):
                    if filename in file:
                        f = open('classes_and_files/temp_dir/'+file, "r")
                        for line in f:
                            if re.search(to_search, line, re.IGNORECASE):
                                dict["Results"].append(line)
                        f.close()
                        TelegramDumpFinder.__clear_cache()
                        return dict
            
            elif Mongo.exists(filename) and not os.path.exists('classes_and_files/temp_dir'):
                print("-----------------Debug message: dump presente su Mongo")
                Mongo.mongo_get(filename)
                for file in os.listdir('classes_and_files/temp_dir'):
                    if filename in file:
                        f = open('classes_and_files/temp_dir/'+file, "r")
                        for line in f:
                            if re.search(to_search, line, re.IGNORECASE):
                                dict["Results"].append(line)
                        f.close()
                        TelegramDumpFinder.__clear_cache()
                        return dict
                        
    @staticmethod     
    async def test(self):
        Mongo.mongo_expire()

    def __clear_cache():
        
        """
        Metodo adibito alla rimozione della cartella temporanea
        """

        if os.path.exists('classes_and_files/temp_dir'):
            shutil.rmtree('classes_and_files/temp_dir')