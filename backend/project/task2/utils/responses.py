from json import dumps
from datetime import datetime as dt
from flask import Response
import mimetypes

class RESTErrorException(Exception):
    def __init__(self, code: int, error: str, message: str, detail: str=None, timestamp=dt.now() ):
        self.code = code
        self.error = error
        self.message = message
        self.detail = detail
        self.timestamp = timestamp.isoformat()
    
    def to_json(self):
        return dumps(obj={
                        "error": self.error,
                        "message": self.message,
                        "detail": self.detail, 
                        "timestamp": self.timestamp
                        })  

    def json_resp(self):
        return Response(
            self.to_json(), status=self.code, mimetype='application/json')

class RESTJSONResponse:
    def __init__(self, code: int, content: dict, mimetype: str = "application/json"):
        self.code: int = code
        self.content = content
        self.mimetype = mimetype
        
        if self.mimetype not in mimetypes.types_map.values():
            raise ValueError(f"Invalid mimetype: {self.mimetype}")
    
    def to_json(self):
        return dumps(self.content)
    
    def json_resp(self):
        return Response(response=self.to_json(), status=self.code, mimetype=self.mimetype)