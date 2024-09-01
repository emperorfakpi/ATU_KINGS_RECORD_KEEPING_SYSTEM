from app import db

# Drop all existing tables (optional)
db.drop_all()

# Create new tables
db.create_all()

print("Database tables created.")
