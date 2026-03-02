from app.persistence.repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository

class HBnBFacade:
    """Facade pattern for business logic."""
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()
    
    # User methods
    def create_user(self, user_data):
        from app.models.user import User
        user = User(**user_data)
        return self.user_repo.add(user)
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_email(email)
    
    def get_all_users(self):
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)
    
    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)
    
    # Place methods
    def create_place(self, place_data):
        from app.models.place import Place
        place = Place(**place_data)
        return self.place_repo.add(place)
    
    def get_place(self, place_id):
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)
    
    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)
    
    # Review methods
    def create_review(self, review_data):
        from app.models.review import Review
        review = Review(**review_data)
        return self.review_repo.add(review)
    
    def get_review(self, review_id):
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        return self.review_repo.get_by_place(place_id)
    
    def update_review(self, review_id, review_data):
        return self.review_repo.update(review_id, review_data)
    
    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
    
    # Amenity methods
    def create_amenity(self, amenity_data):
        from app.models.amenity import Amenity
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)
    
    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)
    
    def get_all_amenities(self):
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)
    
    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)
