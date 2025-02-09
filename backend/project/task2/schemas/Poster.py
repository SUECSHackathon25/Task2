from marshmallow.fields import Nested
from task2.database import ma
from task2.models.Poster import Poster



class PosterSchema(ma.Schema):
    class Meta:
        model = Poster
        include_relationships = True
        load_instance = True
        fields = ['id', 'title', 'abstract', 'advisor_id', 'program_id']
        
posters_schema = PosterSchema(many=True)
