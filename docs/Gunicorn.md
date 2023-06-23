### open domotic-server directory
> cd /home/admin/Repos/domotic-server

### Activate venv
> source venv/bin/activate

### Updating pip
> python -m pip install --upgrade pip

### Install gunicorn module
> python -m pip install gunicorn

### Run RESTful API Server in guinicorn
> sudo venv/bin/gunicorn --workers 10 --bind=0.0.0.0:5000 wsgi:app

### Run RESTful API Server in guinicorn detached
> sudo venv/bin/gunicorn --workers 10 --bind=0.0.0.0:5000 wsgi:app --daemon

### Kill detached gunicorn
> sudo pkil gunicorn
