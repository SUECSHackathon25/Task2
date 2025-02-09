from flask import Blueprint, request
from logging import getLogger

from sqlalchemy.exc import NoResultFound
from task2.judges.utils import save_judge_scores
from task2.models.Judge import Judge
from task2.utils.responses import RESTErrorException, RESTJSONResponse
from task2.database import db
from task2.schemas.Judge import judges_schema, judge_schema


logger = getLogger(__name__)

judge_bp = Blueprint(name='judges', import_name=__name__, url_prefix='/api/judges')


@judge_bp.route(rule='', methods=['GET'])
def get_judges():
    try: 
        with db.session() as s:
            judges = s.query(Judge).all()
            judges_json = judges_schema.dump(judges)
                         
            
            return RESTJSONResponse(code=200, content=judges_json).json_resp()
    except RESTErrorException as e:
        return e.json_resp()
    except Exception as e:
        logger.error(e)
        return RESTErrorException(500, error="Internal Server Error", message="Failed to get judges", detail=f'{e}').json_resp()
      
@judge_bp.route(rule='/<int:judge_id>/posters', methods=['GET'])  
def get_judge_posters(judge_id: int):
    try: 
        with db.session() as s:
            judge = s.query(Judge).filter_by(id=judge_id).one()
            judge_json = judge_schema.dump(judge)            
            return RESTJSONResponse(code=200, content=judge_json).json_resp()
    except NoResultFound:
        return RESTErrorException(404, error="Not Found", message="Judge Not Found", detail=f'Judge {judge_id} not found on server').json_resp()

    except RESTErrorException as e:
        return e.json_resp()
    except Exception as e:
        logger.error(e)
        return RESTErrorException(500, error="Internal Server Error", message="Failed to get judges", detail=f'{e}').json_resp()

@judge_bp.route(rule='/<int:judge_id>/posters', methods=['POST'])  
def process_judge_scores(judge_id: int):
    try: 
        
        save_judge_scores(judge_id=judge_id, data=request.get_json())
                
        return RESTJSONResponse(code=201, content={"success": "ok", "message": "Scores inputted"}).json_resp()
    except NoResultFound:
        return RESTErrorException(404, error="Not Found", message="Judge Not Found", detail=f'Judge {judge_id} not found on server').json_resp()

    except RESTErrorException as e:
        return e.json_resp()
    except Exception as e:
        logger.error(e)
        return RESTErrorException(500, error="Internal Server Error", message="Failed to get judges", detail=f'{e}').json_resp()
        