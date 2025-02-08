from localoka_service.daos import Daos
from localoka_service.exceptions import DataNotFound
from app import elastic_search
from datetime import datetime

class LogDaos(Daos):
    
	_list_index = [
		"transaction"
	]

	_payload_types = [
		"received", "request_to_service", "response_from_service", 
		"request_to_third_party", "response_from_third_party", "response"
	]

	_payload_schema_fields = {
		"type": {"type": "keyword"}, # Jenis Payload (_payload_types)
		"payload": {"type": "keyword"},
		"note": {"type": "text"},
		"title": {"type": "text"},
	}

	_base_schema_fields = {
		"timestamp": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
		"method": {"type": "keyword"},
		"path": {"type": "keyword"},
		"payloads": {
			"type": "nested",
			"properties": _payload_schema_fields
		},
		"level": {"type": "keyword"},
		"status_code": {"type": "integer"},
		"elapsed_time": {"type": "float"},
		"service": {"type": "keyword"}, # Sesuai Index Tersedia (_list_index)
		"additional_details": {"type": "text"}, # Berisi Attribute Detail Lainnya. Format JSON
	}
    
	@classmethod
	def list(cls, filter: dict) -> dict:
		"""
			get list log
		"""
        # Filter Service
		indexes = []
		if filter.get("service"):
			if filter.get("service") in cls._list_index :
				indexes = [filter.get("service")]
		else :
			indexes = cls._list_index
		indexes = [f"{index}_logs" for index in indexes]
        # End Filter Service
        
        # Get Logs
		logs = elastic_search.getAllRecord(
      		indexes=indexes,
			only=["method", "path", "status_code", "timestamp", "level", "service"]
        )

		# Build Data Response
		logs = [{
            "id": log.get("_id"),
            "timestamp": log["_source"].get("timestamp"),
            "method": log["_source"].get("method"),
            "path": log["_source"].get("path"),
            "status_code": log["_source"].get("status_code"),
            "level": log["_source"].get("level"),
            "service": log["_source"].get("service")
		} for log in logs]
        
        # Return Result With Pagination
		return cls._paginate(logs)
    
	@classmethod
	def get(cls, id: str) -> any: # Buat Schema Data Log
		"""
			get log by id
		"""
		# Get Log
		record = elastic_search.getRecordById(id)
  
		# Check Record
		if not record:
			return None

		# Build Data Response
		log = {
            "id": record.get("_id"),
            "timestamp": datetime.fromisoformat(record["_source"].get("timestamp")),
            "method": record["_source"].get("method"),
            "path": record["_source"].get("path"),
            "status_code": record["_source"].get("status_code"),
            "level": record["_source"].get("level"),
            "service": record["_source"].get("service"),
            "payloads": record["_source"].get("payloads"),
            "additional_details": record["_source"].get("additional_details"),
            "elapsed_time": record["_source"].get("elapsed_time")
		}
  
		# Return Result
		return log
    
	@classmethod
	def add(cls, service: str, payload: dict) -> str:
		"""
			add log
		"""
		index_name = f"{service}_logs"
		id = elastic_search.addRecord(index_name, payload)
		return id

	def _paginate(records: list) -> dict :
		return records

