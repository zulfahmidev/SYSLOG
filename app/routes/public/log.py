from . import bp
from app.modules import log
from app.schema.log import LogSchema
from flask import jsonify, current_app, request
 
@bp.route('/log', methods=['GET'])
def get_list_log():  
	return jsonify({
		"data": log.getListLog(request.args)
	}), 200

@bp.route('/log/<string:id>', methods=['GET'])
def get_log_by_id(id):
  	return jsonify({
		"data": LogSchema().dump(log.getLogById(id))
	}), 200