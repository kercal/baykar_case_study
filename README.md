# Case Study

## Installation

These are the windows commands, it can be a bit different with Mac and Linux.

1. Clone git repo to PC:
    ```
    git clone https://git.cs.uni-kl.de/agile-methoden-2/ss22/team/pam-ii.git
    cd Baykar - Case Study
    cd pam
    ```
2. Install the actual Python version: https://www.python.org/downloads/


    python --version
    ```
    

4. Create a Virtual Environment. All Python packages that we need for our project are stored in this folder:
    ```
    python -m venv pam_venv
    ```

5. Now we can activate the environment:
    ```
    pam_venv\Scripts\activate
    ```

    You can tell that it is activated by the ```(pam_env)``` in the command line. The Virtual Environment should always be active when you do anything in the terminal on the project so that all packages are found and new installed packages are saved there.

6. All Python packages I have used so far in the project are stored in the requirements.txt file. You can simply download these into your     virtual environment (this must be activated for this!):
    ```
    pip3 install -r requirements.txt
    ```

    > **_Note:_**  If ```pip3```doesn't work, try instead ```pip```.

7. Create sqlite database:
    ```
    cd pam
    python manage.py migrate
    ```
    Now the file db.sqlite3 has been created, which stores all the database tables.

## Start local server
```
python manage.py runserver
```

Current status of the project can be seen in the browser at http://localhost:8000.


## Django admin

You can access the Django admin interface at http://localhost:8000/admin.

For that, a superuser needs to be created:
```
python manage.py createsuperuser
```

Remarks:

-Since I wasn't expecting a case study right after the day I applied, I noticed it a bit late so in reality I had a lot less time than 3 days.
-I used some code snippets from one of **_My Own_** personal projects that was quite similar to the case study, I didn't use any template or code from the internet, so that's why some of the codes are in German or extra, I wanted to refactor it but with little time that was the best I could do.
-Instead of Postgresql, I used the default sqlite database but it can be converted very easily.
-For some reason there is a bug with usernames. When somebody publishes a post, the username is shown as None so I can't link it to the profile. I'm pretty sure this can also be fixed quickly.