## Install Gunicorn

### Activate venv
> source venv/bin/activate

### Install gunicorn module
> sudo python -m pip install gunicorn

### Run RESTful API Server in guinicorn
> sudo guinicorn --bind=0.0.0.0:5000 app:app


