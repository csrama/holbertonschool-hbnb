from app.extensions import db
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'name': self.name,
            'description': self.description
        })
        return base_dict
