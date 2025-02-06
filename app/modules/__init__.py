log = None

def init_modules(app):
	global log
	with app.app_context():
		from .log import LogModule
  
		log = LogModule(app)
