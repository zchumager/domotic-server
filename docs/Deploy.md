### Kill detached gunicorn
> sudo pkil gunicorn

# Obtain latest changes from master branch
> git pull origin

### Run RESTful API Server in guinicorn detached
> sudo venv/bin/gunicorn --workers 20 --bind=0.0.0.0:5000 wsgi:app --daemon