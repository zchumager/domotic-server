### open domotic-server directory
> cd /home/admin/Repos/domotic-server

### Create venv
> sudo python -m venv venv

### Activate venv (Linux)
> source venv/bin/activate

### Install dependencies
> sudo python -m pip install -r requirements.txt

### Run CLI in venv
> sudo python cli.py --devices

### Run Web API in venv
> sudo python -m venv/bin/flask run --host=0.0.0.0
OR
> sudo python app.py

### Run gunicorn in venv
> sudo venv/bin/gunicorn --workers 10 --bind=0.0.0.0:5000 wsgi:app
