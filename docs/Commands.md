### Scan network to get connected devices
> sudo nmap -snP <raspberry.pi.ip.address>/24

### Create venv in domotic-server folder
> python -m venv venv

### Activate venv in domotic-server folder
> source venv/bin/active

### Install dependencies as sudo
> python -m pip install -r requirements.txt

### Run CLI as sudo with venv to get network devices after venv activation
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python cli.py --connected_macs

### Run CLI as sudo with venv to get registered network devices devices after venv activation
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python cli.py --registered_connected_macs

### Run Web API (sudo is required because of nmap) with venv devices after venv activation
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python -m flask run --host=0.0.0.0
OR
> sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python app.py

### Run gunicorn in venv devices after venv activation
> sudo venv/bin/gunicorn --workers 10 --bind=0.0.0.0:5000 wsgi:app

### Restart bash terminal
> exec $SHELL

## exit venv
>  deactivate

### Restart Raspberry
> sudo reboot now
