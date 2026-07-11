from app.db.database import SessionLocal
from app.repositories.user import UserRepository

db = SessionLocal()

repo = UserRepository()

user = repo.create(
    db=db,
    name="Mahendra",
    email="mahendra@gmail.com",
    password="hashed_password"
)

print(user.id)
print(user.name)
print(user.email)

db.close()