# app/persistence/repository.py
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class BaseRepository:
    """Generic repository for CRUD operations"""
    def __init__(self, model):
        self.model = model

    def get_by_id(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def create(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

class PlaceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Place)

class ReviewRepository(BaseRepository):
    def __init__(self):
        super().__init__(Review)

class AmenityRepository(BaseRepository):
    def __init__(self):
        super().__init__(Amenity)
