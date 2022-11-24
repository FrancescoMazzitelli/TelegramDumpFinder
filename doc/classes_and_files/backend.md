Module classes_and_files.backend
================================

Classes
-------

`TelegramDumpFinder()`
:   

    ### Static methods

    `download_dump(filename, to_search)`
    :   Metodo che effettua l'operazione di grep su un file di interesse. 
        I possibili casi d'uso del metodo sono: 
        1) Sul filesystem esiste una cartella con all'interno i file da greppare 
        2) Il file d'interesse non esiste nè su Mongo nè sul file system 
        viene quindi scaricato da telegram, pushato su Mongo per elaborazioni
        future e infine greppato 
        3) il file d'interesse esiste su Mongo, viene quindi recuperato e greppato
        
        :param filename: Nome del file da cercare sia localmente sia su telegram a seconda dei casi
        :param to_search: Stringa da trovare nel file d'interesse per grep
        :return: Dict che verrà poi spedito tramite HTTP

    `expire_data(self)`
    :   Metodo che controlla se i dump nel database sono scaduti o meno

    `find_dump(filename)`
    :   Metodo che indirizza la ricerca di un dump su Telegram
        
        :param filename: Il nome del dump da cercare su Telegram