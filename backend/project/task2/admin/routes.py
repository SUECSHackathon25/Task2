from flask import Blueprint, Response, current_app, request
from json import dumps
from logging import getLogger

from werkzeug.datastructures.file_storage import FileStorage

from task2.utils.responses import RESTErrorException, RESTJSONResponse

from task2.models.Department import Department 
from task2.models.Judge import Judge 
from task2.models.Poster import Poster 
from task2.models.Program import Program 
from task2.models.Scoring import Scoring 
from task2.models.User import User

from task2.database import db

from task2.admin.utils import process_judges_file



logger = getLogger(__name__)

admin_bp = Blueprint(name='/admin', import_name=__name__, url_prefix='/api/admin')


@admin_bp.route("/setup", methods=["POST"])
def setup_application(): 
    try: 
        #note to self, cancel if database tables exist etc
        logger.info("Creating tables that do not exist")
        with current_app.app_context():
            db.create_all()
            
            with db.session() as s:
                user = User(username="admin", admin=True)
                s.add(user)
                s.commit()
            
            
            return RESTJSONResponse(code=201, content={"message": "Application Setup"}).json_resp()
    except Exception as e: 
        
        return RESTErrorException(500, error="Internal Server Error", message="database failed to be created", detail=f'{e}').json_resp()
    
    
@admin_bp.route("/judges", methods=["POST"])
def import_judges():
    
    
    try: 
        # add in xlsx validation if time
        file: FileStorage = request.files["file"]
        logger.debug(file)
        process_judges_file(file=file)
        
        return RESTJSONResponse(code=201, content={"message": "File Accept"}).json_resp()
    except RESTErrorException as e:
        return e.json_resp()
    except Exception as e:
        logger.error(e)
        return RESTErrorException(500, error="Internal Server Error", message="Failed to upload file", detail=f'{e}').json_resp()
        
        



@admin_bp.route("/posters", methods=["POST"])
def import_posters():
    pass

@admin_bp.route("/matching")
def import_matching():
    pass