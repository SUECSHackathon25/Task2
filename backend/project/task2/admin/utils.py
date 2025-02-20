import io
import random
from typing import List
import pandas as pd
from logging import getLogger
import re
from sqlalchemy import func
from werkzeug.datastructures.file_storage import FileStorage
from sqlalchemy.orm import Session
from openpyxl import Workbook



from task2.database import db
from task2.models.Program import Program
from task2.models.Poster import Poster
from task2.models.Department import Department
from task2.models.Judge import Judge
from task2.models.User import User
from task2.models.Score import Score
from task2.utils.helpers import evalute_env_bool


from task2.utils.responses import RESTErrorException

logger = getLogger(__name__)


def sanitize_name(str)->str:
    return re.sub(r'[^\w]', '', str).lower()

def process_judges_file(file: FileStorage):
    df = pd.read_excel(file, engine='openpyxl')
    
    with db.session() as s:
        '''
        delete old judges out of system first 
        '''
        s.query(Score).delete()
        s.query(Poster).delete()
        s.query(Judge).delete()
        s.commit()
    
        if 'judge' not in df.columns:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'judge'. NOTE IS CASE SENSITIVE" )     
        if 'judge firstname' not in df.columns:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'judge firstname'. NOTE IS CASE SENSITIVE" )     
        if 'judge lastname' not in df.columns:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column  'judge lastname'. NOTE IS CASE SENSITIVE" )     
        if 'department' not in df.columns:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'department'. NOTE IS CASE SENSITIVE" )     

        for _,row in df.iterrows():
            username = sanitize_name(f"{row['judge firstname']}{row['judge lastname']}".replace(" ", ""))
        
            user: User = s.query(User).filter_by(username=username).first()
            if not user:
                user = User(username=username)
                s.add(user)
                s.commit()
                logger.info(f"User created for judge {row['judge firstname']} {row['judge lastname']}")
            department: Department = s.query(Department).filter_by(name=row["department"]).first()
            if not department:
                department = Department(name=row["department"])
                s.add(department)
                s.commit()
                logger.info(f"Created department: {department}")
            
            judge = Judge(id=row['judge'], first_name=row['judge firstname'], last_name=row['judge lastname'], department=department, user=user)
            s.add(judge)
            s.commit()
            logger.info(f"Created judge: {judge}")
                
def process_posters_file(file: FileStorage):
    df = pd.read_excel(file, engine='openpyxl')
    # df.columns = df.columns.str.lower()

    with db.session() as s:
        
        judges = s.query(Judge).all()
        
        if not judges:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="No Judges in Database", detail="Cannot upload posters before judges")
        s.query(Score).delete()
        s.query(Poster).delete()
        s.commit()
        logger.info(msg="Deleting old posters out of database")

        
        
        if 'poster #' not in df.columns:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'poster #'. NOTE IS CASE SENSITIVE" )        
        if 'title' not in df.columns:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'title'. NOTE IS CASE SENSITIVE" )   
        if 'abstract' not in df.columns:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'abstract'. NOTE IS CASE SENSITIVE" )        
        if 'advisor firstname' not in df.columns:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'advisor firstname'. NOTE IS CASE SENSITIVE" ) 
        if 'advisor lastname' not in df.columns:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'advisor lastname'. NOTE IS CASE SENSITIVE" ) 
        if 'judge-1' not in df.columns:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'judge-1'. NOTE IS CASE SENSITIVE" ) 
        if 'judge-2' not in df.columns:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'judge-2'. NOTE IS CASE SENSITIVE" ) 
        if 'program' not in df.columns:
            raise RESTErrorException(code=422, error="Unprocessable Entity", message="Missing Column name", detail="Missing excel column 'program'. NOTE IS CASE SENSITIVE" ) 

        for _,row in df.iterrows():
            
            advisor_uname = sanitize_name(f"{row['advisor firstname']}{row['advisor lastname']}".replace(" ", ""))
            advisor = s.query(Judge).join(User).filter_by(username=advisor_uname).first()
         
            judge1_uname = sanitize_name(f"{row['judge-1']}".replace(" ", ""))
            judge1 = s.query(Judge).join(User).filter_by(username=judge1_uname).first()
            if not judge1:
                raise RESTErrorException(code=404, error="Not Found", message="Judge 1 Not Found", detail=f"Judge1 {judge1_uname} Not Found for Poster # {row['poster #']}" ) 
            
            
            judge2_uname = sanitize_name(f"{row['judge-2']}".replace(" ", ""))
            judge2 = s.query(Judge).join(User).filter_by(username=judge2_uname).first()
            if not judge2:
                raise RESTErrorException(code=404, error="Not Found", message="Judge 2 Not Found", detail=f"Judge2 {judge2_uname} Not Found for Poster #{row['poster #']}" ) 
            
            if judge1 == judge2:
                raise RESTErrorException(code=409, error="Conflict", message="Conflict", detail=f"Judges of Poster #{row['poster #']} matching" )     
            if judge1 == advisor or judge2 == advisor:
                raise RESTErrorException(code=409, error="Conflict", message="Conflict", detail=f"Either Judge 1 or Judge 2 is listed as Advisor of Poster #{row['poster #']}" )     

            
            program: Program = s.query(Program).filter_by(title=row["program"]).first()
            if not program:
                program = Program(title=row["program"])
                s.add(instance=program)
                s.commit()
                logger.info(msg=f"Created program: {program}")
            
            
            poster = Poster(id=row["poster #"], title=row['title'],abstract=row['abstract'], advisor=advisor, program=program)
            s.add(poster)
            s.commit()
            for judge in [judge1, judge2]:
                assign_judge(poster=poster, judge=judge, s=s)

            score_conflict_check(s)
    
            
            
            
def assign_judge(poster: Poster, judge: Judge, s: Session):
    
    existing_scores: List[Score] = s.query(Score).filter_by(poster=poster).all()
    
    if len(existing_scores) > 2:
        raise RESTErrorException(code=400, error="Bad Request", message="Too many judges", detail=f"Too many judges assigned to Poster #{poster.id}" ) 
    elif existing_scores == 1 and existing_scores[0].judge == judge:
        raise RESTErrorException(code=409, error="Conflict", message="Conflict", detail=f"Judges of Poster #{poster.id} matching" )     
    else: 
        # add in score
        score = Score(poster=poster, judge=judge)
        
        s.add(score)
        s.commit()        
        
    
            
def score_conflict_check(s: Session): 
    result = s.query(
        Score.poster_id,
        func.count(func.distinct(Score.judge_id)).label('distinct_judges')
    ).group_by(Score.poster_id).having(
        func.count(func.distinct(Score.judge_id)) != 2  # Filter posters that don't have exactly 2 distinct judges
    ).all()
    
    if result != []:
        bad_poster_ids = [poster_id for poster_id in result]
        
        raise RESTErrorException(code=400, error="Bad Request", message="Bad Judge Assignments", detail=f"Following Posters have invalid judge assignments: {bad_poster_ids}" ) 


def process_results():

    with db.session() as s:
        
        posters = s.query(Poster).all()
        judges = s.query(Judge).all()
        headers = ['PosterID'] + [judge.id for judge in judges]
        df = pd.DataFrame(columns=headers)
        for poster in posters:
            
            row_data = pd.Series([0] * len(judges), index=headers[1:], dtype=int)
            row_data['PosterID'] = poster.id
            for score in poster.scores:
                if score.score:  #wont cause Nan if null
                    row_data[score.judge_id] = int(score.score)
            df = pd.concat([df, row_data.to_frame().T], ignore_index=True)

        if evalute_env_bool("GENERATE_RANDOM", "False"):
            df = df.applymap(lambda x: random.randint(1, 10) if x == 0 else x)


        file_stream = io.BytesIO()
        df.to_excel(file_stream, index=False, engine='openpyxl')  # Write to the byte stream
        file_stream.seek(0)
    return file_stream