from typing import Any
from app.models.base_model import BaseModel
from app.extensions import db

class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), nullable=False)   # FK لاحقًا
    place_id = db.Column(db.String(36), nullable=False)  # FK لاحقًا

    def __init__(self, text: str, rating: int, user_id: str, place_id: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
        self.validate()

    def validate(self):
        if not self.text.strip(): raise ValueError("text required")
        if not (1 <= self.rating <= 5): raise ValueError("rating must be 1..5")
        if not self.user_id.strip(): raise ValueError("user_id required")
        if not self.place_id.strip(): raise ValueError("place_id required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
