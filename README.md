# fleamarket

Piattaforma di acquisti online di articoli da collezionismo, di antiquariato o riuso. Il sito consente di mettere in
contatto i venditori con i possibili acquirenti. Per installarlo è sufficiente unzippare la directory (o clonare la repo
github https://github.com/vitto-canta/djangoProject_bootstrap) e aprirla con Pycharm (o eventualmente altro).
Per configurare il virtualenv è possibile sfruttare quello già fornito (directory \venv) adatto a sistemi operativi Unix,
in alternativa crearne uno nuovo e procedere all'installazione dei requirements, riportati nel file requirements.txt

per fare ciò, attivare il virtualenv e optare per una delle due opzioni:
- installare i requirements singolarmente con il comando pip install <nome_plugin>
- installarli tutti insieme con il comando pip install -r requirements.txt

Infine avviare il server con il comando python manage.py runserver

Lascio a disposizione utente admin:

- username: admin
- password: admin

E utente venditore e compratore (non superuser):

- username: test
- password: test1234!
