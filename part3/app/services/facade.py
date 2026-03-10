from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.extensions import bcrypt
from app.persistence.repository import UserRepository, PlaceRepository, ReviewRepository, AmenityRepository


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
        return {
            "id": user.id,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }, 201

    def get_all_users(self):
        users = self.users.get_all()
        return [
            {
                "id": u.id,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "email": u.email,
                "created_at": u.created_at.isoformat(),
                "updated_at": u.updated_at.isoformat()
            } for u in users
        ]

    # ---------------- PLACES ----------------
    def create_place(self, user_id: str, **data):
        place = Place(
            title=data['name'],
            price=data.get('price', 0.0),
            latitude=data.get('latitude', 0.0),
            longitude=data.get('longitude', 0.0),
            owner_id=user_id,
            description=data.get('description', "")
        )
        self.places.create(place)
        return place

    def get_places_by_user(self, user_id: str):
        user = self.users.get_by_id(user_id)
        return user.places if user else []

    # ---------------- REVIEWS ----------------
    def create_review(self, user_id: str, **data):
        review = Review(
            text=data['text'],
            rating=data['rating'],
            user_id=user_id,
            place_id=data['place_id']
        )
        self.reviews.create(review)
        return review

    def get_reviews_for_place(self, place_id: str):
        place = self.places.get_by_id(place_id)
        return place.reviews if place else []

    # ---------------- AMENITIES ----------------
    def create_amenity(self, **data):
        amenity = Amenity(
            name=data['name'],
            description=data.get('description', "")
        )
        self.amenities.create(amenity)
        return amenity

    def get_amenities_for_place(self, place_id: str):
        place = self.places.get_by_id(place_id)
        return place.amenities if place else []
