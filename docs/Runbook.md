### open domotic-server directory
> cd /home/admin/Repos/domotic-server

### Run Home Assistant detached
> sudo docker compose up -d

### Create venv
> python3 -m venv venv

### Activate venv (Linux)
> source venv/bin/activate

### Install dependencies in venv 
> python3 -m pip install -r requirements.txt

### Run CLI as sudo with venv to get network devices
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python cli.py --all_devices

### Run CLI as sudo with venv to get registered network devices
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python cli.py --registered_connected

### Run python cronjob script as sudo for single execution with venv
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python cronjob.py

### Run Web API (sudo is required because of nmap) with venv
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python -m flask run --host=0.0.0.0
OR
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python app.py

### Run gunicorn (sudo is required because of nmap) with venv
> sudo venv/bin/gunicorn --workers 10 --bind=0.0.0.0:5000 wsgi:app

### Run gunicorn (sudo is required because of nmap) detached with venv
> sudo venv/bin/gunicorn --workers 10 --bind=0.0.0.0:5000 wsgi:app --daemon

### Kill detached gunicorn if needed
> sudo pkill gunicorn


### Enable cronjob in crontab
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python cli.py--crontab

### Disable cronjob in crontab
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python cli.py--quitcron
