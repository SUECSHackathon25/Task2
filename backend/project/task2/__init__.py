from flask import Flask
from psycopg2 import OperationalError
from sqlalchemy import text
from werkzeug.exceptions import HTTPException
from logging import getLogger


from config import App
from task2.database import db, ma
from task2.utils.responses import RESTErrorException, RESTJSONResponse

from flask_cors import CORS


logger = getLogger(__name__)

def create_app():
    # create and configure the app
    app = Flask(import_name=__name__)
    if App.mode == 'development':
        app.debug = True
        app.logger.setLevel(level="DEBUG")
        logger.debug('Application in debug mode')
    app.config.from_object(obj=App)
    db.init_app(app=app)
    ma.init_app(app=app)

    CORS(app)
    # healthcheck, so only internal    
    @app.route('/healthcheck')
    def healthcheck():
        '''
        Healthcheck on server.
        Moved here to prevent circular import issues over fetching celery status
        '''
        try:
            # Check database connection
            db.session.execute(statement=text(text="SELECT 1"))
            db_status = "OK"
        except OperationalError as e:
            db_status = str(e)
        
        healthcheck = {
            "flask": "ok",
            "db": db_status
        }
        RESTJSONResponse(code=200, content=healthcheck).json_resp()
        
       # return Response(response=dumps(obj={"flask": "ok", "db": db_status}), status=200, mimetype='application/json')
  
    @app.after_request
    def add_x_clacks_overhead(response):
        response.headers['X-Clacks-Overhead'] = 'GNU Terry Pratchett'
        return response
    
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(500)
    def http_error_handler(error: HTTPException):
            logger.debug("handing error")
            return RESTErrorException(
                error.code, error=error.name, message=error.description
            ).json_resp()
    
    '''
    Blueprint imports - probably over complicated for small project, but easier to expand on later if desired
    '''
    
    from task2.admin.routes import admin_bp
    from task2.judges.routes import judge_bp
    app.register_blueprint(blueprint=admin_bp)
    app.register_blueprint(blueprint=judge_bp)
    
    return app