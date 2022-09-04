### open domotic-server directory
> cd /home/admin/Repos/domotic-server

### Create venv
> python -m venv venv

### Activate venv (Linux)
> source venv/bin/activate

### Install dependencies
> sudo python -m pip install -r requirements.txt

## for installing a new dependency
> sudo python -m pip install

### Run RESTful API Server
> sudo python -m flask run --host=0.0.0.0
OR
> sudo python app.py

## Get devices from CLI
> sudo python cli --devices