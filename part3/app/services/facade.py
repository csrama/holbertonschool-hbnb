from app.persistence.repository import (
    UserRepository,
    PlaceRepository,
    ReviewRepository,
    AmenityRepository
)
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.extensions import bcrypt


class HBnBFacade:
    def __init__(self):
        self.users = UserRepository()
        self.places = PlaceRepository()
        self.reviews = ReviewRepository()
        self.amenities = AmenityRepository()

    # ---------------- USERS ----------------
    def create_user(self, data: dict) -> tuple[dict, int]:
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
        user.set_password(data['password'])
        self.users.create(user)
        return user.to_dict(), 201

    def get_user_by_email(self, email: str):
        user = self.users.get_by_email(email)
        return user.to_dict() if user else None

    def get_user_by_id(self, user_id: str):
        user = self.users.get_by_id(user_id)
        return user.to_dict() if user else None

    # ---------------- PLACES ----------------
    def create_place(self, user_id: str, **data) -> tuple[dict, int]:
        place = Place(
            title=data['name'],
            price=data.get('price', 0.0),
            latitude=data.get('latitude', 0.0),
            longitude=data.get('longitude', 0.0),
            owner_id=user_id,
            description=data.get('description', "")
        )
        self.places.create(place)
        return place.to_dict(), 201

    def get_place_by_id(self, place_id: str):
        place = self.places.get_by_id(place_id)
        return place.to_dict() if place else None

    def get_places_by_owner(self, owner_id: str):
        return [p.to_dict() for p in self.places.get_by_owner(owner_id)]

    # ---------------- REVIEWS ----------------
    def create_review(self, user_id: str, **data) -> tuple[dict, int]:
        review = Review(
            text=data['text'],
            rating=data['rating'],
            user_id=user_id,
            place_id=data['place_id']
        )
        self.reviews.create(review)
        return review.to_dict(), 201

    def get_review_by_id(self, review_id: str):
        review = self.reviews.get_by_id(review_id)
        return review.to_dict() if review else None

    def get_reviews_by_place(self, place_id: str):
        return [r.to_dict() for r in self.reviews.get_by_place(place_id)]

    def get_reviews_by_user(self, user_id: str):
        return [r.to_dict() for r in self.reviews.get_by_user(user_id)]

    # ---------------- AMENITIES ----------------
    def create_amenity(self, **data) -> tuple[dict, int]:
        amenity = Amenity(
            name=data['name'],
            description=data.get('description', "")
        )
        self.amenities.create(amenity)
        return amenity.to_dict(), 201

    def get_amenity_by_id(self, amenity_id: str):
        amenity = self.amenities.get_by_id(amenity_id)
        return amenity.to_dict() if amenity else None

    def get_all_amenities(self):
        return [a.to_dict() for a in self.amenities.get_all()]
