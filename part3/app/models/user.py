#!/usr/bin/python3
"""User model with SQLAlchemy and password hashing - Tasks 1 & 6"""

from __future__ import annotations

import re
from typing import Any, List, TYPE_CHECKING

from app.extensions import db, bcrypt
from .base_model import BaseModel

if TYPE_CHECKING:
    from .place import Place
    from .review import Review


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    """
    User entity with SQLAlchemy mapping and password hashing.
    
    Attributes:
        first_name (str): User's first name (required, max 50)
        last_name (str): User's last name (required, max 50)
        email (str): User's email address (required, unique, valid format)
        password (str): Hashed password (stored securely)
        is_admin (bool): Admin privileges flag (default False)
    """
    
    # ==================== TASK 6: SQLAlchemy Columns ====================
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # ==================== TASK 8: Relationships - Amaal ====================
    places  = db.relationship('Place',  backref='owner', lazy=True,
                          cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user',  lazy=True,
                          cascade='all, delete-orphan')

    # ==================== TASK 1: Password Hashing ====================

    def __init__(self, **kwargs):
        """Initialize a new User."""
        # Extract password if present (for hashing)
        password = kwargs.pop('password', None)
        
        # Initialize BaseModel first
        super().__init__(**kwargs)
        
        # Validate email format
        if self.email and not _EMAIL_RE.match(self.email):
            raise ValueError("email must be a valid email address")
        
        # Hash password if provided (Task 1)
        if password:
            self.hash_password(password)

    def hash_password(self, password: str) -> None:
        """Hashes the password before storing it. (Task 1)"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Verifies if the provided password matches the hashed password. (Task 1)"""
        return bcrypt.check_password_hash(self.password, password)

    # ==================== Business Methods ====================

    def get_full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"

    # ==================== Serialization ====================

    def to_dict(self) -> dict:
        """Convert user to dictionary WITHOUT password."""
        base_dict = super().to_dict()
        base_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
        })
        return base_dict

    # ============= Magic Methods =============

    def __str__(self) -> str:
        return f"[User] {self.email}"

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
