# tests/test_crud_clean.py
from app import create_app
from app.extensions import db, bcrypt
from app.services.facade import HBnBFacade
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

app = create_app("development")
facade = HBnBFacade()

with app.app_context():
    print("\n STARTING CLEAN CRUD TESTS \n")

    # ---------- RESET DATABASE ----------
    db.drop_all()
    db.create_all()
    print("Database reset completed.\n")

    # ------------------ USERS ------------------
    print("Users CRUD")

    user_data = {"first_name": "Test", "last_name": "User", "email": "test@hbnb.com", "password": "123456"}
    user, status = facade.create_user(user_data)
    print("Created User:", user)

    read_user = User.query.filter_by(email="test@hbnb.com").first()
    print("Read User:", read_user.first_name, read_user.last_name)

    read_user.first_name = "UpdatedTest"
    db.session.commit()
    print("Updated User:", read_user.first_name)

    db.session.delete(read_user)
    db.session.commit()
    print("Deleted User:", read_user.email)

    # ------------------ PLACES ------------------
    print("\n Places CRUD")

    user_for_place = facade.create_user({"first_name": "Owner", "last_name": "One", "email": "owner@hbnb.com", "password": "123456"})[0]

    place = facade.create_place(
        user_id=user_for_place["id"],
        name="Test Place",
        description="A nice test place",
        price=50.0,
        latitude=24.7,
        longitude=46.6
    )
    print("Created Place:", place.to_dict())

    read_place = Place.query.get(place.id)
    read_place.price = 75.0
    db.session.commit()
    print("Updated Place:", read_place.price)

    db.session.delete(read_place)
    db.session.commit()
    print("Deleted Place:", read_place.name)

    # ------------------ REVIEWS ------------------
    print("\n Reviews CRUD")

    place_for_review = facade.create_place(
        user_id=user_for_place["id"],
        name="Review Place",
        price=60.0,
        latitude=24.7,
        longitude=46.6
    )
    review = facade.create_review(
        user_id=user_for_place["id"],
        text="Awesome place!",
        rating=5,
        place_id=place_for_review.id
    )
    print("Created Review:", review.to_dict())

    read_review = Review.query.get(review.id)
    read_review.rating = 4
    db.session.commit()
    print("Updated Review:", read_review.rating)

    db.session.delete(read_review)
    db.session.commit()
    print("Deleted Review:", read_review.text)

    # ------------------ AMENITIES ------------------
    print("\n Amenities CRUD")

    amenity = facade.create_amenity(name="Gym", description="Fitness room")
    print("Created Amenity:", amenity.to_dict())

    read_amenity = Amenity.query.get(amenity.id)
    read_amenity.description = "Updated Fitness room"
    db.session.commit()
    print("Updated Amenity:", read_amenity.description)

    db.session.delete(read_amenity)
    db.session.commit()
    print("Deleted Amenity:", read_amenity.name)

    print("\n CLEAN CRUD TESTS COMPLETED SUCCESSFULLY!")
