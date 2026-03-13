"""
Facade pattern for HBnB application.
Provides a unified interface to the business logic layer.
"""
from app.persistence.repository import BaseRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """Facade for HBnB application - handles all business logic"""
    
    def __init__(self):
        """Initialize repositories"""
        self.user_repo = BaseRepository(User)
        self.place_repo = BaseRepository(Place)
        self.review_repo = BaseRepository(Review)
        self.amenity_repo = BaseRepository(Amenity)
    
    # ========== User Methods ==========
    
    def create_user(self, user_data):
        """Create a new user"""
        user = User(**user_data)
        return self.user_repo.create(user)
    
    def get_user(self, user_id):
        """Get a user by ID"""
        return self.user_repo.get_by_id(user_id)
    
    def get_user_by_email(self, email):
        """Get a user by email"""
        # Note: You may need to implement this in BaseRepository
        return User.query.filter_by(email=email).first()
    
    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        """Update a user"""
        user = self.get_user(user_id)
        if user:
            for key, value in user_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            db.session.commit()
        return user
    
    def delete_user(self, user_id):
        """Delete a user"""
        user = self.get_user(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    
    # ========== Place Methods ==========
    
    def create_place(self, place_data):
        """Create a new place"""
        place = Place(**place_data)
        return self.place_repo.create(place)
    
    def get_place(self, place_id):
        """Get a place by ID"""
        return self.place_repo.get_by_id(place_id)
    
    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):
        """Update a place"""
        place = self.get_place(place_id)
        if place:
            for key, value in place_data.items():
                if hasattr(place, key):
                    setattr(place, key, value)
            db.session.commit()
        return place
    
    def delete_place(self, place_id):
        """Delete a place"""
        place = self.get_place(place_id)
        if place:
            db.session.delete(place)
            db.session.commit()
            return True
        return False
    
    def get_places_by_owner(self, owner_id):
        """Get all places by a specific owner"""
        return Place.query.filter_by(owner_id=owner_id).all()
    
    # ========== Review Methods ==========
    
    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()
    
    def get_review(self, review_id):
        """Get a review by ID"""
        return self.review_repo.get_by_id(review_id)
    
    def create_review(self, review_data):
        """Create a new review"""
        review = Review(**review_data)
        return self.review_repo.create(review)
    
    def update_review(self, review_id, review_data):
        """Update a review"""
        review = self.get_review(review_id)
        if review:
            for key, value in review_data.items():
                if hasattr(review, key):
                    setattr(review, key, value)
            db.session.commit()
        return review
    
    def delete_review(self, review_id):
        """Delete a review"""
        review = self.get_review(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
            return True
        return False
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        return Review.query.filter_by(place_id=place_id).all()
    
    def get_reviews_by_user(self, user_id):
        """Get all reviews by a specific user"""
        return Review.query.filter_by(user_id=user_id).all()
    
    # ========== Amenity Methods ==========
    
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.create(amenity)
    
    def get_amenity(self, amenity_id):
        """Get an amenity by ID"""
        return self.amenity_repo.get_by_id(amenity_id)
    
    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()
    
    def get_amenity_by_name(self, name):
        """Get an amenity by name"""
        return Amenity.query.filter_by(name=name).first()
    
    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        amenity = self.get_amenity(amenity_id)
        if amenity:
            for key, value in amenity_data.items():
                if hasattr(amenity, key):
                    setattr(amenity, key, value)
            db.session.commit()
        return amenity
    
    def delete_amenity(self, amenity_id):
        """Delete an amenity"""
        amenity = self.get_amenity(amenity_id)
        if amenity:
            db.session.delete(amenity)
            db.session.commit()
            return True
        return False
