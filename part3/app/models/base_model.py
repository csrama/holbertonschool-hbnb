#!/usr/bin/python3

from datetime import datetime
import uuid

from app.extensions import db


class BaseModel(db.Model):
    """Base class for all HBnB entities with SQLAlchemy mapping."""
    
    __abstract__ = True  # This class won't create a table in DB

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        """Initialize base model with optional kwargs."""
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        
        # Ensure id is set
        if not self.id:
            self.id = str(uuid.uuid4())
        
        # Set timestamps if not provided
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()

    def save(self):
        """Save changes to database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete from database."""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
