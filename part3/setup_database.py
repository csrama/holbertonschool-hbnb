#!/usr/bin/env python3
"""
HBnB - Database Setup Script
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from config import DevelopmentConfig
from app.extensions import db, bcrypt
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
import uuid

def main():
    print("\n" + "="*60)
    print("HBnB Database Setup")
    print("="*60)

    app = create_app("development")

    with app.app_context():
        try:
            # Step 1: Drop & Create tables
            print("\nDropping existing tables...")
            db.drop_all()
            print("Creating fresh tables...")
            db.create_all()
            print("✅ Tables ready!")

            # Step 2: Create Users
            print("\n📝 Creating users...")

            # Admin user (is_admin=True)
            admin = User(
                id=str(uuid.uuid4()),
                first_name='Raghad',
                last_name='Almalki',
                email='raghad@hbnb.com',
                is_admin=True
            )
            admin.password = 'admin123'
            db.session.add(admin)

            jana = User(
                id=str(uuid.uuid4()),
                first_name='Jana',
                last_name='Bakri',
                email='jana@hbnb.com',
                is_admin=False
            )
            jana.password = 'jana123'
            db.session.add(jana)

            rama = User(
                id=str(uuid.uuid4()),
                first_name='Rama',
                last_name='Alshahri',
                email='rama@hbnb.com',
                is_admin=False
            )
            rama.password = 'rama123'
            db.session.add(rama)

            db.session.commit()
            print(f"✅ Created {User.query.count()} users")

            # Step 3: Create Amenities
            print("\n📝 Creating amenities...")

            amenities_names = ['WiFi', 'Pool', 'Parking', 'Breakfast', 'Gym', 'AC']
            amenities = {}

            for name in amenities_names:
                a = Amenity(
                    id=str(uuid.uuid4()),
                    name=name
                )
                db.session.add(a)
                amenities[name] = a

            db.session.commit()
            print(f"✅ Created {Amenity.query.count()} amenities")

            # Step 4: Create Places
            print("\n📝 Creating places...")

            place1 = Place(
                id=str(uuid.uuid4()),
                title='Luxury Resort Riyadh',
                description='A luxury resort in the heart of Riyadh with all modern amenities.',
                price=100.0,
                latitude=24.7136,
                longitude=46.6753,
                owner_id=admin.id
            )
            place1.amenities.append(amenities['WiFi'])
            place1.amenities.append(amenities['Pool'])
            place1.amenities.append(amenities['Parking'])
            place1.amenities.append(amenities['Breakfast'])
            db.session.add(place1)

            place2 = Place(
                id=str(uuid.uuid4()),
                title='Modern City Hotel',
                description='A modern hotel in the city center with a great view.',
                price=100.0,
                latitude=24.7242,
                longitude=46.6385,
                owner_id=admin.id
            )
            place2.amenities.append(amenities['WiFi'])
            place2.amenities.append(amenities['Parking'])
            place2.amenities.append(amenities['Gym'])
            db.session.add(place2)

            place3 = Place(
                id=str(uuid.uuid4()),
                title='Cozy Downtown Apartment',
                description='Comfortable apartment in the city center, suitable for families.',
                price=50.0,
                latitude=24.7353,
                longitude=46.5752,
                owner_id=admin.id
            )
            place3.amenities.append(amenities['WiFi'])
            place3.amenities.append(amenities['AC'])
            db.session.add(place3)

            place4 = Place(
                id=str(uuid.uuid4()),
                title='Family Villa with Garden',
                description='Luxury family villa with a spacious garden.',
                price=10.0,
                latitude=24.6877,
                longitude=46.7219,
                owner_id=admin.id
            )
            place4.amenities.append(amenities['WiFi'])
            place4.amenities.append(amenities['Pool'])
            place4.amenities.append(amenities['Parking'])
            db.session.add(place4)

            place5 = Place(
                id=str(uuid.uuid4()),
                title='Budget Room Near Metro',
                description='An economy room close to the metro.',
                price=90.0,
                latitude=24.7500,
                longitude=46.6900,
                owner_id=admin.id
            )
            place5.amenities.append(amenities['WiFi'])
            db.session.add(place5)

            db.session.commit()
            print(f"✅ Created {Place.query.count()} places")

            # Step 5: Create Reviews
            print("\n📝 Creating reviews...")

            reviews_data = [
                (place1.id, jana.id,  5, 'Amazing place! Highly recommended.'),
                (place1.id, rama.id,  4, 'Great experience, clean and lovely service.'),
                (place2.id, rama.id,  4, 'Beautiful hotel with a great location.'),
                (place3.id, jana.id,  5, 'Very comfortable apartment at a reasonable price.'),
                (place4.id, jana.id,  5, 'Luxurious villa! We loved the garden.'),
            ]

            for place_id, user_id, rating, text in reviews_data:
                review = Review(
                    id=str(uuid.uuid4()),
                    place_id=place_id,
                    user_id=user_id,
                    rating=rating,
                    text=text
                )
                db.session.add(review)

            db.session.commit()
            print(f"✅ Created {Review.query.count()} reviews")

            # Summary
            print("\n" + "="*60)
            print("🎉 Database setup completed successfully!")
            print("="*60)
            print("\n📋 Login Credentials:")
            print("-" * 60)
            print("  raghad@hbnb.com  | admin123  | 👑 Admin (Raghad)")
            print("  jana@hbnb.com    | jana123   | 👤 User (Jana)")
            print("  rama@hbnb.com    | rama123   | 👤 User (Rama)")
            print("-" * 60)
            print(f"\n📊 Summary:")
            print(f"   Users:     {User.query.count()}")
            print(f"   Places:    {Place.query.count()}")
            print(f"   Reviews:   {Review.query.count()}")
            print(f"   Amenities: {Amenity.query.count()}")
            print("\n" + "="*60 + "\n")

            return 0

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return 1

if __name__ == '__main__':
    exit(main())
