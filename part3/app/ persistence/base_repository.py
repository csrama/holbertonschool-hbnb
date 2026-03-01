from abc import ABC, abstractmethod
from app.extensions import db

class BaseRepository(ABC):
    """Base repository interface."""
    
    @abstractmethod
    def add(self, obj):
        pass
    
    @abstractmethod
    def get(self, obj_id):
        pass
    
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def update(self, obj_id, data):
        pass
    
    @abstractmethod
    def delete(self, obj_id):
        pass

class SQLAlchemyRepository(BaseRepository):
    """SQLAlchemy implementation of repository."""
    
    def __init__(self, model):
        self.model = model
    
    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj
    
    def get(self, obj_id):
        return self.model.query.get(obj_id)
    
    def get_all(self):
        return self.model.query.all()
    
    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key) and key != 'id':
                    setattr(obj, key, value)
            db.session.commit()
        return obj
    
    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False
