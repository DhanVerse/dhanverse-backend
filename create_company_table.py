from app.db.database import Base, engine

# Import models
from app.models.user import User
from app.models.company import Company

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Done!")