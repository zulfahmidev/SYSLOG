from . import bp
from app.modules import log
from flask import jsonify, current_app, request


@bp.route('/', methods=['GET'])
def handle_root():
	return jsonify({
		"service": current_app.config["APP_NAME"],
		'message': 'OK'
	})
