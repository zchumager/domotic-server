### Scan network to get connected devices
> sudo nmap -snP <raspberry.pi.ip.address>/24

### Create venv in domotic-server folder
> python -m venv venv

### Activate venv in domotic-server folder
> source venv/bin/active

### Install dependencies as sudo
> python -m pip install -r requirements.txt

### Run CLI as sudo with venv to get network devices
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python cli.py --all_devices

### Run CLI as sudo with venv to get registered network devices
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python cli.py --registered_devices

### Run Web API (sudo is required because of nmap) with venv
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python -m flask run --host=0.0.0.0
OR
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python app.py

### Run gunicorn in venv
> sudo venv/bin/gunicorn --workers 10 --bind=0.0.0.0:5000 wsgi:app

### Restart bash terminal
> exec $SHELL

### Restart Raspberry
> sudo reboot now
