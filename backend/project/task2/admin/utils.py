from os import name
import pandas as pd
from logging import getLogger

import openpyxl
from werkzeug.datastructures.file_storage import FileStorage

from task2.database import db
from task2.models.Department import Department
from task2.models.Judge import Judge
from task2.models.User import User

from task2.utils.responses import RESTErrorException

logger = getLogger(__name__)


def process_judges_file(file: FileStorage):
    df = pd.read_excel(file, engine='openpyxl')
    
    with db.session() as s:
        '''
        delete old judges out of system first 
        '''
        s.query(Judge).delete()
        s.commit()
    
    if 'Judge FirstName' not in df.columns:
        raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'Judge FirstName'. NOTE IS CASE SENSITIVE" )     
    if 'Judge LastName' not in df.columns:
        raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column  'Judge LastName'. NOTE IS CASE SENSITIVE" )     
    if 'Department' not in df.columns:
        raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'department'. NOTE IS CASE SENSITIVE" )     

    for _,row in df.iterrows():
  
            
        username = f"{row['Judge FirstName']}{row['Judge LastName']}"
        
        
        with db.session() as s:
            user: User = s.query(User).filter_by(username=username).first()
            if not user:
                user = User(username=username)
                s.add(user)
                s.commit()
                logger.info(f"User created for judge {row['Judge FirstName']} {row['Judge LastName']}")
            department: Department = s.query(Department).filter_by(name=row["Department"]).first()
            if not department:
                department = Department(name=row["Department"])
                s.add(department)
                s.commit()
                logger.info(f"Created department: {department}")
            
            judge = Judge(first_name=row['Judge FirstName'], last_name=row['Judge LastName'], department=department, user=user)
            s.add(judge)
            s.commit()
            logger.info(f"Created judge: {judge}")
            
        
        
    # if REQ_COLUMNS not in [col.lower() for col in list(df.columns)]:
        
    #     logger.debug(df.co)
    #     raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing field names", detail=f"Must contain following columns: {REQ_COLUMNS}")
    
    return