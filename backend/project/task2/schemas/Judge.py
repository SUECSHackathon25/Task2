from marshmallow.fields import Nested
from task2.database import ma
from task2.models.Judge import Judge
from task2.schemas.Score import JudgeScoreSchema


class JudgeSchema(ma.Schema):

    # posters = Nested(PostersSchema, many=True, dump_only=True)  # Nested posters
    scores = Nested(JudgeScoreSchema, many=True, dump_only=True)
    class Meta:
        model = Judge
        include_relationships = True
        fields = ["id", "first_name", "last_name", "scores"]
             
        
judges_schema = JudgeSchema(many=True)
judge_schema = JudgeSchema()