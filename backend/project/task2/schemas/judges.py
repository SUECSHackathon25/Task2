from task2.database import ma
from task2.models.Judge import Judge


class JudgeSchema(ma.Schema):
    model = Judge
    class Meta:
        fields = ["id", "first_name", "last_name"]
        
        
judges_schema = JudgeSchema(many=True)