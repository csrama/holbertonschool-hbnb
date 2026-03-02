"""Association table for many-to-many relationship between Place and Amenity"""
from hbnb.app import db
from app.extensions import db

place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id")),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"))
)
# Association table for many-to-many relationship
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)
