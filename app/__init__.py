import psycogreen.gevent
psycogreen.gevent.patch_psycopg()
from localoka_service import FlaskService
from flask_marshmallow import Marshmallow
from flask_celery import FlaskCelery
from app.config import Config
from app.library.elastic_search import ElasticSearch

celery = FlaskCelery()
marshmallow = Marshmallow()
elastic_search = ElasticSearch(Config)


def create_app(config):
	from app.modules import init_modules
	from app.routes import init_routes

	return FlaskService.create(
		__name__,
		config,
		extensions=[
			marshmallow,
			elastic_search,
			celery
		],
		hook={
			"init_modules": init_modules,
			"init_routes": init_routes
		}
	)

app = create_app(Config)
