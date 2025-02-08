from os import getenv


class App:
    dbHost = getenv(key="DB_HOST", default="database")
    dbPort = getenv(key="DB_PORT", default="5432") 
    dbName = getenv(key="DB_NAME",default="postgres")
    dbUser = getenv(key="DB_USER", default="postgres")
    dbPwd = getenv(key="DB_PWD", default="postgres")
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{dbUser}:{dbPwd}@{dbHost}:{dbPort}/{dbName}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    mode = getenv(key="MODE", default="development")
    loggingConfig = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}