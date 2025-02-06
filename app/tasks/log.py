from app import celery
from app.modules import log
from marshmallow import ValidationError
from flask import current_app

@celery.task(name="save_log", queue="syslog")
def save_log(payload):
	"""
		antrian untuk add log
	"""
	print(payload)
	try:
		result = log.addLog(payload)
		print("Berhasil:", result)
	except ValidationError as errors:  
		return False
		# return {
		# 	"message": "Invalid fields in payloads.",
		# 	"errors": errors
		# }
	return True
