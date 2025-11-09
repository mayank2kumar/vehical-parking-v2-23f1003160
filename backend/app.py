import json
import random
from datetime import datetime, timedelta

from faker import Faker
from applications import app, db, User
from applications.models import Location, ParkingLot, ParkingSpot, ReservedParking

fake = Faker()

# ✅ 1. Create Admin If Not Exists
def create_admin():
    with app.app_context():
        db.create_all()
        existing_admin = User.query.filter_by(admin=True).first()
        if not existing_admin:
            admin = User(
                name="Admin",
                username="admin",
                email="admin@mayank.com",
                password="admin123",
                admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created successfully.")
        else:
            print("ℹ️ Admin already exists.")


# ✅ 2. Create Random Non-admin Users
def create_users(num_users=5):
    with app.app_context():
        existing_users = User.query.filter_by(admin=False).count()
        if existing_users >= num_users:
            print("ℹ️ Enough users already exist.")
            return

        for _ in range(num_users):
            user = User(
                name=fake.name(),
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password="1234",
                admin=False
            )
            db.session.add(user)
        db.session.commit()
        print(f"✅ {num_users} dummy users added.")


# ✅ 3. Seed Custom Data From JSON
def seed_custom_data_from_json(json_file="parking_data.json"):
    with app.app_context():
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"❌ JSON file not found: {json_file}")
            return

        db.create_all()

        if Location.query.count() > 0:
            print("ℹ️ Custom data already seeded — skipping.")
            return

        for loc in data.get("locations", []):
            location = Location(
                name=loc["name"],
                city=loc["city"],
                latitude=loc.get("latitude"),
                longitude=loc.get("longitude")
            )
            db.session.add(location)
            db.session.commit()

            for lot_data in loc.get("lots", []):
                lot = ParkingLot(
                    prime_location_name=lot_data["prime_location_name"],
                    price=lot_data["price"],
                    address=lot_data["address"],
                    pin_code=lot_data["pin_code"],
                    number_of_spots=lot_data["number_of_spots"]
                )
                lot.location_id = location.id
                db.session.add(lot)
                db.session.commit()

                for _ in range(lot_data["number_of_spots"]):
                    spot = ParkingSpot(lot_id=lot.id, is_available=True)
                    db.session.add(spot)
                db.session.commit()

        print("✅ Custom parking data seeded successfully.")


# ✅ 4. Add Random Reservations
def create_random_reservations(max_reservations=10):
    with app.app_context():
        users = User.query.filter_by(admin=False).all()
        all_spots = ParkingSpot.query.all()

        if not users or not all_spots:
            print("⚠️ No users or spots available to create reservations.")
            return

        reserved_count = 0
        for _ in range(min(max_reservations, len(all_spots))):
            user = random.choice(users)
            spot = random.choice(all_spots)

            # Skip already reserved spots
            if not spot.is_available:
                continue

            park_time = datetime.now() - timedelta(hours=random.randint(1, 24))
            reservation = ReservedParking(
                user_id=user.id,
                spot_id=spot.id,
                park_time=park_time,
                exit_time=None,
                total_cost=None
            )
            spot.is_available = False
            db.session.add(reservation)
            db.session.add(spot)
            reserved_count += 1

        db.session.commit()
        print(f"✅ {reserved_count} random reservations created.")


# ✅ 5. Main Runner
if __name__ == "__main__":
    create_admin()
    create_users(num_users=8)
    seed_custom_data_from_json()
    create_random_reservations(max_reservations=15)
    app.run(debug=True)
