#!/usr/bin/python3

from __future__ import annotations

from typing import Any

from app.extensions import db
from .base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity entity with SQLAlchemy mapping.
    
    Attributes:
        name (str): Name of the amenity (required, max 50)
        description (str): Description of the amenity (optional, max 200)
    """
    
    __tablename__ = 'amenities'

    # ==================== TASK 7: SQLAlchemy Columns ====================
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    # Relationships (to be implemented in Task 8)
    # places = db.relationship('Place', secondary='place_amenity', backref='amenities', lazy=True)

    def __init__(self, **kwargs):
        """
        Initialize a new Amenity with validation.
        
        Raises:
            ValueError: If validation fails for any field
        """
        super().__init__(**kwargs)

        # ============= Validation =============
        # Name validation
        if not self.name or not self.name.strip():
            raise ValueError("name is required")
        if len(self.name) > 50:
            raise ValueError("name must be at most 50 characters")
        self.name = self.name.strip()

        # Description validation (optional)
        if self.description and len(self.description) > 200:
            raise ValueError("description must be at most 200 characters")
        if self.description:
            self.description = self.description.strip()

    # ============= Serialization =============

    def to_dict(self) -> dict:
        """Convert amenity to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "description": self.description,
        })
        return base_dict

    # ============= Magic Methods =============

    def __str__(self) -> str:
        return f"[Amenity] {self.name}"

    def __repr__(self) -> str:
        return f"<Amenity id={self.id} name={self.name}>"
