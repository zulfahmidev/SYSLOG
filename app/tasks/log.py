from app import celery
from app.modules import log
from marshmallow import ValidationError
from flask import current_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery.task(name="save_log", queue="syslog")
def save_log(**payload):
	"""
		Antrian untuk add log
	"""
	try:
		log.addLog(payload)
	except ValidationError as errors:  
		logger.error(errors)
		return False
	except Exception as errors:  
		logger.error(errors)
		return False
	return True
