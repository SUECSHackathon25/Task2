from flask import Blueprint, current_app, request, send_file
from logging import getLogger

from sqlalchemy import false, inspect
from werkzeug.datastructures.file_storage import FileStorage

from task2.utils.responses import RESTErrorException, RESTJSONResponse

from task2.models.Department import Department 
from task2.models.Judge import Judge 
from task2.models.Poster import Poster 
from task2.models.Program import Program 
from task2.models.Score import Score 
from task2.models.User import User

from task2.database import db

from task2.admin.utils import process_judges_file, process_posters_file, process_results



logger = getLogger(__name__)

admin_bp = Blueprint(name='admin', import_name=__name__, url_prefix='/api/admin')



@admin_bp.route("/setup", methods=["GET"])
def check_if_application_init(): 
    try: 
        inspector = inspect(db.engine)

        tables = inspector.get_table_names()
        
        if tables: 
            return RESTJSONResponse(code=200, content={"message": "Application Setup"}).json_resp()
        else: 
            return RESTErrorException(404, error="Not Found", message="No tables in the database, must be created").json_resp()
    except Exception as e: 
        logger.debug(e)
        return RESTErrorException(500, error="Internal Server Error", message="Database check failed", detail=f'{e}').json_resp()
    
    



@admin_bp.route("/setup", methods=["POST"])
def setup_application(): 
    try: 
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
        process_judges_file(file=file)
        
        return RESTJSONResponse(code=201, content={"message": "File Accepted"}).json_resp()
    except RESTErrorException as e:
        return e.json_resp()
    except Exception as e:
        logger.error(e)
        return RESTErrorException(500, error="Internal Server Error", message="Failed to upload judges file", detail=f'{e}').json_resp()
        
        



@admin_bp.route("/posters", methods=["POST"])
def import_posters():
    try: 
        # add in xlsx validation if time
        file: FileStorage = request.files["file"]
        process_posters_file(file=file)
        
        return RESTJSONResponse(code=201, content={"message": "File Accepted"}).json_resp()
    except RESTErrorException as e:
        return e.json_resp()
    except Exception as e:
        with db.session() as s:
            s.query(Poster).delete()
        return RESTErrorException(500, error="Internal Server Error", message="Failed to upload posters file", detail=f'{e}').json_resp()
        


@admin_bp.route("/results", methods=["GET"])
def get_results():
    
    
    try:   
        file = process_results()
        return send_file(file,as_attachment=True, download_name="results.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")    
    except RESTErrorException as e:
        return e.json_resp()
    except Exception as e:
        logger.error(e)
        return RESTErrorException(500, error="Internal Server Error", message="Failed to upload judges file", detail=f'{e}').json_resp()
        
        
