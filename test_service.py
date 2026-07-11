from app.db.database import SessionLocal
from app.services.auth import AuthService
from app.schemas.auth import UserRegister

db = SessionLocal()

service = AuthService()

user = UserRegister(
    name="Rahul",
    email="rahul@gmail.com",
    password="Rahul@123"
)

created_user = service.register(
    db=db,
    user=user
)

print(created_user.id)
print(created_user.name)
print(created_user.email)

db.close()