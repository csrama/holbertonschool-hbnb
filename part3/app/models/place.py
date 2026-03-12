#!/usr/bin/python3

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

from app.persistence.repository import (
    UserRepository,
    PlaceRepository,
    ReviewRepository,
    AmenityRepository
)

class HBnBFacade:
    def __init__(self):
        self.users = UserRepository()
        self.places = PlaceRepository()
        self.reviews = ReviewRepository()
        self.amenities = AmenityRepository()

    # USERS
    def get_all_users(self):
        return self.users.get_all()

    def get_user(self, user_id):
        return self.users.get_by_id(user_id)

    # PLACES
    def get_all_places(self):
        return self.places.get_all()

    def get_place(self, place_id):
        return self.places.get_by_id(place_id)

    # REVIEWS
    def get_reviews_for_place(self, place_id):
        return self.reviews.get_by_place(place_id)

    # AMENITIES
    def get_all_amenities(self):
        return self.amenities.get_all()


facade = HBnBFacade()
