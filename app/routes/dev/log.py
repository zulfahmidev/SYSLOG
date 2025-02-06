from . import bp
from app import celery
from app.modules import log
from marshmallow import ValidationError
from flask import jsonify, request
 
@bp.route('/log', methods=['POST'])
def add_log():
    try:
        payload = request.get_json()
        
        log.addLog(payload)
        return jsonify({
            "message": "Log has been added successfully"
        }), 200
    except ValidationError as e:
        return jsonify({
            "error": e.messages
        }), 400
        

@bp.route('/log/async', methods=['POST'])
def add_log_async():
    payload = request.get_json()
    
    celery.send_task(
        "save_log",
        kwargs=payload,
        queue="syslog"
    )
    return jsonify({
        "message": "Log has been added successfully"
    }), 200