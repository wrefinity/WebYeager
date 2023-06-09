# yeag_sliper   `webapp`


## getting started with the yeager_ai app

## Requirements

1. python 3.8 above
2. Postgres

## Installation and Setup

## create a postgres database named "project"

```# window user
psql -U postgres
create database project;
```


```# Linux user
sudo -i -u postgres
psql
create database project;
CREATE USER yeager WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE project TO yeager;
# for test user creation
ALTER USER yeager CREATEDB;
```


### create a virtual environment and activate

first change directory into yeager_ai

```#bash
cd yeager_ai
```

```# bash- Windows
python -m venv venvpython3 -m venv .venv
# activate enviroment
. venv/Scripts/activate
```

````
```# Linux
sudo apt-get install python3-venv
python3 -m venv .venv
# activate enviroment
source .venv/bin/activate
````

```# macOS
python3 -m venv .venv
# activate enviroment
source .venv/bin/activate
```

### install requirement

```#bash
cd requirements
pip install -r base.txt
pip install -r local.txt
pip install dj-stripe slippers 'celery[redis]' python-decouple
```

Note: on installing slippers you need to add it to installed apps under the setting of the entry app point yeager_ai

### before running the app update your password to match your postgres user password

1. locate the base.py file in the config direction and update your password for the postgres user

### Apply Migration

```
python manage.py makemigrations
python manage.py migrate
```

### for djstripe payment 
add the secret key to the administrator dashboard then run the script below scripts to synchronize payment models
``` # stop the server before sync
python manage.py djstripe_sync_models
```


### Running the app

```#bash
python manage.py runserver
```

### running celery window user
``` # on a  new terminal 
cd yeager_ai
python -m celery -A config.celery worker --loglevel=info
```
### running celery linux/mac user
``` # on a  new terminal 
cd yeager_ai
celery -A config.celery worker --loglevel=info
```
