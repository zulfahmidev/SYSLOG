from localoka_service.module import BaseModule
from app.daos.log import LogDaos
from localoka_service.exceptions import DataNotFound
from app.schema.log import LogSchema, LogPayloadSchema
from werkzeug.exceptions import BadRequest
from marshmallow import Schema, fields, validate, ValidationError
import json

class LogModule(BaseModule):
    
    def addLog(self, payload: dict) -> bool :
        # Validate
        data = LogSchema().load(payload)               
        try :
            # Save To ES
            result = LogDaos.add(data.get('service'), data)
            if not result :
                raise Exception(f"Index {data.get('service')}_logs does not exists")
        except Exception as e:
            raise BadRequest(f"Something wrong when add log: {e}")
    
    def getListLog(self, filter: dict) -> list :
        try :
            logs = LogDaos.list(filter)
            return logs
        except Exception as e:
            raise BadRequest(f"Something wrong when get list log: {e}")
    
    def getLogById(self, id: str) -> dict :
        
        # Get Log Data
        try :
            log = LogDaos.get(id)
        except Exception as e:
            raise BadRequest(f"Something wrong when get log by id: {e}")
        
        # Check Log Data
        if log is None :
            raise DataNotFound("ID does not exists.")
        
        # Return Log Data
        return log
    