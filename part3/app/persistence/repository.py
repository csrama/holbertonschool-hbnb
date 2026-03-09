from app.extensions import db
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class PlaceRepository:
    def create(self, place: Place):
        db.session.add(place)
        db.session.commit()
        return place

    def get_by_id(self, place_id: str):
        return Place.query.get(place_id)

    def get_all(self):
        return Place.query.all()

class ReviewRepository:
    def create(self, review: Review):
        db.session.add(review)
        db.session.commit()
        return review

    def get_by_id(self, review_id: str):
        return Review.query.get(review_id)

    def get_all(self):
        return Review.query.all()

class AmenityRepository:
    def create(self, amenity: Amenity):
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def get_by_id(self, amenity_id: str):
        return Amenity.query.get(amenity_id)

    def get_all(self):
        return Amenity.query.all()
