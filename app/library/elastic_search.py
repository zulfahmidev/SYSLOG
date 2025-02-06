from app.config import Config
from elasticsearch import Elasticsearch # type: ignore
from typing import Optional

class ElasticSearch() :
    
    _default_size=99
    
    def __init__(self, config: Config) -> None:
        self._host = config.ES_HOST
        self._port = config.ES_PORT
        self._createConnection()
    
    def _createConnection(self) -> None :
        self._connection = Elasticsearch(
            f"http://{self._host}:{self._port}", 
            verify_certs=False)
    
    def getAllRecord(self, indexes: list = [], query: dict = {}, only: list = [], options: dict = {}) -> list :  
        if (len(indexes) == 0) :
            return []
        
        if not query :
            query =  {
                "match_all": {}
            }
            
        body = {
            "query": query,
            "from": options.get('offset') or 0,
            "size": options.get('limit') or self._default_size,
            "sort": options.get('sort') or {}
        }
        
        if len(only) > 0 :
            body["_source"] = only
        
        result = self._connection.search(
            index=indexes, 
            body=body, 
        )
        
        records = [hit for hit in result["hits"]["hits"]]
        return records
    
    def getRecordById(self, id:str) -> any :
        result = self._connection.search(
            index="*", 
            body={
                "query": {
                    "term": {
                        "_id": id
                    }
                },
                "size": 1
            }, 
        )
        if len(result["hits"]["hits"]) > 0 :
            return result["hits"]["hits"][0]
        return None
    
    def createIndex(self, index_name: str, properties: dict) -> bool :
        if not self._connection.indices.exists(index=index_name):
            self._connection.indices.create(index=index_name, body={
                "mappings": {
                    "properties": properties
                }
            })
            return True
        return False
    
    def addRecord(self, index_name: str, data: any) -> Optional[str] :
        if self._connection.indices.exists(index=index_name):
            return self._connection.index(index=index_name, body=data)
        return None

    def clearIndex(self, index_name: str) :
        self._connection.delete_by_query(index=index_name, body={"query": {"match_all": {}}})
