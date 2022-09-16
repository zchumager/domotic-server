### open domotic-server directory
> cd /home/admin/Repos/domotic-server

### Create venv
> python -m venv venv

### Activate venv (Linux)
> source venv/bin/activate

### Install dependencies in venv
> (venv) python -m pip install -r requirements.txt

### Run CLI 
> sudo python cli.py --devices

### Run Web API (sudo is required because of nmap)
> sudo python -m venv/bin/flask run --host=0.0.0.0
OR
> sudo python app.py

### Run gunicorn (sudo is required because of nmap)
> sudo venv/bin/gunicorn --workers 10 --bind=0.0.0.0:5000 wsgi:app
