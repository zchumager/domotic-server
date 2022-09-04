### open domotic-server directory
> cd /home/admin/Repos/domotic-server

### Activate venv
> source venv/bin/activate

### Install gunicorn module
> sudo python -m pip install gunicorn

### Run RESTful API Server in guinicorn
> sudo guinicorn --workers 10 --bind=0.0.0.0:5000 wsgi:app
