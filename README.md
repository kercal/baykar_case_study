# PAM II

## Installation

Ich habe hier jeweils nur die Linux/MacOS Befehle reingepackt, unter Windows können die eventuell ein wenig abweichen.

1. Das Git Repository auf euren PC klonen:
    ```
    git clone https://git.cs.uni-kl.de/agile-methoden-2/ss22/team/pam-ii.git
    cd pam-ii
    ```
2. Auf den Branch dev wechseln:
    ```
    git checkout dev
    ```

3. Installiere die aktuelle Python-Version (3.10.4): https://www.python.org/downloads/

    Ob du schon die richtige Python Version installiert hast, kannst du mit
    ```
    python3 --version
    ```
    prüfen.


4. Erstelle eine Virtual Environment. In diesem Ordner werden alle Python Pakete gespeichert, die wir für unser Projekt brauchen:
    ```
    python3 -m venv pam_venv
    ```

5. Nun kannst du die Virtual Environment aktivieren:
    ```
    source pam_venv/bin/activate
    ```

    An dem ```(pam_env)```in der Kommandozeile erkennst du, dass sie aktiviert ist.
    Die Virtual Environment sollte immer aktiv sein, wenn du irgendetwas im Terminal am Projekt machst, damit alle Pakete gefunden werden und damit neue installierte Pakete dort gespeichert werden. 

6. In der Datei requirements.txt sind alle bisher von uns verwendeten Python Pakete im Projekt hinterlegt.
    Diese kannst du nun einfach in deine Virtual Environment herunterladen (dazu muss diese aktiviert sein!):
    ```
    pip3 install -r requirements.txt
    ```

    Wenn du ein neues Paket installiert hast, kannst du die requirements.txt Datei updaten:
    ```
    pip3 freeze > requirements.txt
    ```
    > **_Hinweis:_**  Falls ```pip3```nicht funktioniert, versuche stattdessen ```pip```.

7. Erstelle sqlite Datenbank:
    ```
    cd pam
    python manage.py migrate
    ```
    Nun wurde die Datei db.sqlite3 erstellt, die alle Datenbanktabellen speichert.

## Starte lokalen Testserver
```
python3 manage.py runserver
```

Nun kannst du im Browser unter http://localhost:8000 den aktuellen Stand der Webseite sehen.

## Django Dokumentation

https://docs.djangoproject.com/en/4.0/

Es gibt ein sehr gutes [Step-by-Step Tutorial](https://docs.djangoproject.com/en/4.0/intro/tutorial01/) für eine Umfragewebseite. Viele der dortigen Schritte sollten bei unserem Projekt sehr ähnlich sein.

## Django admin

Unter http://localhost:8000/admin kann man auf das Admin-Interface von Django zugreifen.

Dazu musst du mit 
```
python manage.py createsuperuser
```
einen Admin Benutzer erstellen.