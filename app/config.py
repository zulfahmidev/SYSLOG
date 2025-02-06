from localoka_service.type.config import (
	ConfigPath,
	BaseConfigCelery,
 	BaseConfigCache,
	BaseConfigGateway
)
import os

class Config(BaseConfigGateway, BaseConfigCelery, BaseConfigCache):
	APP_NAME	= 'Service Syslog'

	@ConfigPath
	@classmethod
	def PATH_APP(cls):
		return os.path.dirname(__file__)

	# Elastic Search Configs
	ES_HOST = os.getenv('ES_HOST')
	ES_PORT = os.getenv('ES_PORT')
 
	# Celery
	CELERY_BEAT_SCHEDULE = {
        "order_scheduler": {
            "task": "order_schedule",
            # "schedule": 30.0,  # every 600 sec or 10 minutes
            "schedule": 600.0,  # every 600 sec or 10 minutes
                    "options": {
                        # "expires" : 55.0
                        "expires": 540.0  # every 540 sec or 9 minutes
                    },
        }
    }

	# prepare role
	API_SERVICE_KEY_OLD	= os.environ.get('API_SERVICE_KEY_OLD')
