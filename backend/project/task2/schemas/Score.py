from marshmallow.fields import Nested
from task2.database import ma
from task2.models.Score import Score
from task2.schemas.Poster import PosterSchema




class JudgeScoreSchema(ma.Schema):
     '''
    Use this when wanting to fetch posters from the judge side, if needed can write another one to get
    judges from a given poster ( might not be needed currently)

    Args:
        ma (_type_): _description_
     '''
     poster = Nested(PosterSchema, dump_only=True)

     class Meta:
        model = Score
        include_relationships = True
        load_instance = True
        fields = ['id', 'score_id', 'score', "poster"]
        


