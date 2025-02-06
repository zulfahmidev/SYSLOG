# localoka-service-syslog

Service yang mengatasi proses yang berhubungan dengan log sistem.

## Referensi
* [Qiscuss-whatsapp-otp](https://www.qiscus.com/id/blog/kirim-whatsapp-otp/)

## Setup development
install python 3.9
```bash
# update system
sudo apt install software-properties-common
sudo apt update -y

# add python repository
sudo add-apt-repository ppa:deadsnakes/ppa

# install python and dep
sudo apt install python3.9
sudo apt-get install -y python3-pip

# check version
python3.9 --version
```
install virtual env
```bash
python3.9 -m pip install --upgrade pip
python3.9 -m pip install pipenv

# check
pipenv --version

# create symlink if cannot call pipenv
sudo ln -s ~/.local/bin/pipenv /usr/bin/pipenv
```
setup environtment
```bash
# activate virtual env
pipenv shell

# install requirements
pip install -r requirements.txt

# create file .flaskenv to set environtment in file
# and copy the environment example bellow
```

flask command
```bash
# runing flask
flask run

# migrate database
flask db migrate -m "comment"

# upgrade database
flask db upgrade

# downgrade database
flask db downgrade
```

celery command
```bash
# run scheduler
celery -A worker:celery beat --loglevel=DEBUG -s <path-to-local-database>

# run worker
celery -A worker:celery worker --loglevel=DEBUG -Q <queue_name>

# sample
celery -A worker:celery worker --loglevel=DEBUG -Q notification
celery -A worker:celery worker --loglevel=DEBUG -Q notification,notification_schedule

celery -A worker:celery beat --loglevel=DEBUG -s data/celery-schedule.db
```

## Environtment

| Name | Value | Description |
| -- | -- | -- |
| FLASK_ENV | development or staging os production | - |
| FLASK_DEBUG | Bool | - |
| API_GATEWAY_HOST | address | API Gateway Host Address |
| API_GATEWAY_PORT | port | API Gateway Port |
| API_SERVICE_KEY | String | Secret key for communication between service |
| DATABASE_HOST | address | Database Host Address |
| DATABASE_PORT | port | Database Port |
| DATABASE_NAME | String | Database Name |
| DATABASE_USER | String | Database user |
| DATABASE_PASS | String | Database password |
| REDIS_HOST | address | Redis Host Address |
| REDIS_PORT | port | Redis Port |
| RABBITMQ_HOST | String | RabbitMQ host |
| RABBITMQ_PORT | Port | RabbitMQ port |
| RABBITMQ_USER | String | RabbitMQ user |
| RABBITMQ_PASS | String | RabbitMQ password |
| RABBITMQ_VHOST | String | RabbitMQ virtual host |
| MAIL_SERVER | address | Mail Host Address |
| MAIL_PORT | port | Mail Port |
| MAIL_USE_TLS | Bool | use TLS connection |
| MAIL_USE_SSL | Bool | use SSL connection |
| MAIL_USERNAME | String | email username |
| MAIL_PASSWORD | String | email password |
| MAIL_DEFAULT_SENDER | String | email sender |

example
```bash
# flask
FLASK_ENV=development
FLASK_DEBUG=True

# api gateway
API_GATEWAY_HOST=localhost
API_GATEWAY_PORT=8000
API_SERVICE_KEY=you-will-never-guess

# database
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
DATABASE_NAME=
DATABASE_USER=root
DATABASE_PASS=root

# redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379

# rabbitmq
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=localoka
RABBITMQ_PASS=password
RABBITMQ_VHOST=localoka

# mail
MAIL_SERVER=localhost
MAIL_PORT=8025
MAIL_USE_TLS=0
MAIL_USE_SSL=0
MAIL_USERNAME=email@example.com
MAIL_PASSWORD=password
MAIL_DEFAULT_SENDER=noreply@localoka.co.id
```
