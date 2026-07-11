from app.schemas.auth import UserRegister

user = UserRegister(
    name="Mahendra",
    email="mahendra@gmail.com",
    password="Mahendra@123"
)

print(user)