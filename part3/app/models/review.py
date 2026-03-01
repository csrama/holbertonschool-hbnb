from __future__ import annotations

from typing import Any

from hbnb.app.models.base_model import BaseModel
from hbnb.app import db


class Review(BaseModel):
    """
    Review entity:
    - text   (required)
    - rating (int 1..5)
    - user_id (foreign key to User)
    - place_id (foreign key to Place)
    Relationships:
    - user: User who wrote the review
    - place: Place being reviewed
    """
    
    __tablename__ = 'reviews'

    # SQLAlchemy columns
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref='reviews', lazy=True)
    place = db.relationship('Place', backref='reviews_list', lazy=True)  # Different backref name

    def __init__(
        self,
        text: str,
        rating: int,
        user_id: str,
        place_id: str,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
        self.validate()

    def validate(self) -> None:
        """Validate review attributes"""
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("text is required")

        if not isinstance(self.rating, int):
            raise ValueError("rating must be an integer")
        if not (1 <= self.rating <= 5):
            raise ValueError("rating must be between 1 and 5")

        if not isinstance(self.user_id, str) or not self.user_id.strip():
            raise ValueError("user_id is required")

        if not isinstance(self.place_id, str) or not self.place_id.strip():
            raise ValueError("place_id is required")

    def to_dict(self) -> dict[str, Any]:
        """Convert review to dictionary with related data"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name
            } if self.user else None,
            'place': {
                'id': self.place.id,
                'title': self.place.title
            } if self.place else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
