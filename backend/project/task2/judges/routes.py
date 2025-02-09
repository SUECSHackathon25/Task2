from flask import Blueprint
from logging import getLogger


from task2.models.Judge import Judge
from task2.utils.responses import RESTErrorException, RESTJSONResponse
from task2.database import db



logger = getLogger(__name__)

judge_bp = Blueprint(name='judges', import_name=__name__, url_prefix='/api/judges')


@judge_bp.route('', methods=['GET'])
def get_judges():
 
    
    # return
    try: 
        with db.session() as s:
                    judges = s.query(Judge).all()
                    logger.debug(judges)        
            
        return RESTJSONResponse(code=201, content={"message": "File Accept"}).json_resp()
    except RESTErrorException as e:
        return e.json_resp()
    except Exception as e:
        logger.error(e)
        return RESTErrorException(500, error="Internal Server Error", message="Failed to get judges", detail=f'{e}').json_resp()
        
        