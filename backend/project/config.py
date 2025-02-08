from os import getenv

class Config:
    dbHost = getenv(key="DB_HOST", default="database")
    dbPort = getenv(key="DB_PORT", default="5432") 
    dbName = getenv(key="DB_NAME",default="postgres")
    dbUser = getenv(key="DB_USER", default="postgres")
    dbPwd = getenv(key="DB_PWD", default="postgres")
