def init_routes(app):
	from localoka_service.blueprint import errors_blueprint, hooks_blueprint
	from .public import bp as public_blueprint
	from .dev import bp as dev_blueprint
 
	with app.app_context():
		app.register_blueprint(hooks_blueprint)
		app.register_blueprint(errors_blueprint)
		app.register_blueprint(public_blueprint)
		app.register_blueprint(dev_blueprint)
