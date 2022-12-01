from classes_and_files.teleLib import ToScrape
from classes_and_files.mongo_class import Mongo
import os
import re
import shutil

telegram_lib = ToScrape

class TelegramDumpFinder:

    @staticmethod
    async def find_dump(filename):

        """
        Metodo che indirizza la ricerca di un dump su Telegram
        
        :param filename: Il nome del dump da cercare su Telegram
        """

        if filename is not None:
            to_send = await telegram_lib.find_dump(filename)
            print("-----------------Debug message: ricerca dump in corso")
            if to_send is None or len(to_send) == 0: 
                print("-----------------Debug message: dump non trovato, ricerca riferimenti in corso")
                to_sendM = await telegram_lib.message_reader(filename)
                if to_sendM is None or len(to_sendM) == 0:
                    return {"failure_message":"Non e' stato trovato nessun riferimento al file desiderato su Telegram"}
                else: return to_sendM
            else: return to_send  

    @staticmethod
    async def download_dump(filename, to_search):
        
        """
        Metodo che effettua l'operazione di grep su un file di interesse. 
        I possibili casi d'uso del metodo sono: 
        1) Sul filesystem esiste una cartella con all'interno i file da greppare 
        2) Il file d'interesse non esiste nè su Mongo nè sul file system 
        viene quindi scaricato da telegram, pushato su Mongo per elaborazioni
        future e infine greppato 
        3) il file d'interesse esiste su Mongo, viene quindi recuperato e greppato
        
        :param filename: Nome del file da cercare sia localmente sia su telegram a seconda dei casi
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
                response = await telegram_lib.find_dump(filename)
                if response is None or len(response) == 0: 
                    print("-----------------failure_messagge: richiesta non valida: il file cercato non esiste e non può essere scaricato")
                    dict["Results"].append('failure_messagge: richiesta non valida: il file cercato non esiste e non puo\' essere scaricato') 
                    return dict
                else:
                    date = await telegram_lib.download_file(filename)
                    Mongo.mongo_put(filename)
                    if date is not None:
                        for file in os.listdir('classes_and_files/temp_dir'):
                            if filename in file:
                                f = open('classes_and_files/temp_dir/'+file, "r")
                                for line in f:
                                    if re.search(to_search, line, re.IGNORECASE):
                                        dict["Results"].append(line)
                                f.close()
                                TelegramDumpFinder.__clear_cache()
                                return dict
                    else:
                        print("-----------------failure_messagge: richiesta non valida: il file cercato non esiste e non può essere scaricato")
                        dict["Results"].append('failure_messagge: richiesta non valida: il file cercato non esiste e non puo\' essere scaricato') 
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
            else:
                dict["Results"].append("failure_message : Non e' stato trovato nessun riferimento al file desiderato su Telegram")
                return 
                        
    @staticmethod     
    async def expire_data(self):
        
        """
        Metodo che controlla se i dump nel database sono scaduti o meno
        """

        Mongo.mongo_expire()

    def __clear_cache():
        
        """
        Metodo adibito alla rimozione della cartella temporanea
        """

        if os.path.exists('classes_and_files/temp_dir'):
            shutil.rmtree('classes_and_files/temp_dir')