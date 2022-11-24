Module classes_and_files.mongo_class
====================================

Classes
-------

`Mongo()`
:   Classe framework Mongo

    ### Methods

    `exists(file_name)`
    :   Metodo che controlla l'esistenza di un dump sul database
        
        :param file_name: Nome del file da cercare

    `mongo_expire()`
    :   Metodo che rimuove dal database i dump presenti da almeno una settimana e quindi considerati non più aggiornati

    `mongo_get(filename)`
    :   Metodo che recupera un dump dal database e lo salva su una cartella temporanea per effettuare operazioni di scraping
        
        :param filename: Nome del dump da cercare nel database

    `mongo_put(file_name)`
    :   Metodo che inserisce all'interno del database un nuovo dump scaricato in precedenza e posizionato in una cartella temporanea
        
        :param file_name: Il nome del dump collocato nella cartella e da caricare sul database