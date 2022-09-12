### Scan network to get connected devices
> sudo nmap -snP 192.168.1.8/24

### Create venv in domotic-server folder
> python -m venv venv

### Activate venv in domotic-server folder
> source venv/bin/active

### Install dependencies as sudo
> sudo python -m pip install -r requirements.txt

### Run CLI in venv
> sudo python cli.py --devices

### Run Web API in venv
> sudo python -m venv/bin/flask run --host=0.0.0.0
OR
> sudo python app.py

### Run gunicorn in venv
> sudo venv/bin/gunicorn --workers 10 --bind=0.0.0.0:5000 wsgi:app

### Restart Raspberry
> sudo reboot now