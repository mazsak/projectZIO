# projectZIO

## How to run on local machine

```bash
# Requires Python and Git installed!
git clone ...
pip install pipenv
cd app
pipenv install
pipenv shell
python manage.py migrate
python manage.py runserver
```

## How to run in Docker container
```bash
# Requires installed Docker and Docker Compose on local machine!
docker-compose up --build
```

### Creating super user for Django inside Docker container
```bash
# Make sure django_app container is running!
docker exec -it django_app python manage.py createsuperuser
```