
from logging import getLogger


from task2.database import db
from task2.models.Poster import Poster
from task2.models.Judge import Judge
from task2.models.Score import Score


logger = getLogger(__name__)

def save_judge_scores(judge_id: int, data: dict):
    with db.session() as s:
        judge = s.query(Judge).filter_by(id=judge_id).one()
        for entry in data['scores']:
            poster = s.query(Poster).filter_by(id=entry['poster']['id']).first()
            if not poster: 
                raise ValueError("Poster not found in database")
            score = s.query(Score).filter_by(judge=judge, poster=poster).first()
            if not score: 
                raise ValueError("Score not found in database")
            score.score = entry['score']
            s.commit()
            
            
            

    