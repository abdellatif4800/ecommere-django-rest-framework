import os
from dotenv import load_dotenv
import jwt

load_dotenv()

jwt_secret = os.getenv("JWT_SECRET")


def generate_token(payload):
    encoded = jwt.encode(payload, jwt_secret, algorithm="HS256")
    print(jwt.decode(encoded, jwt_secret, algorithms=["HS256"]))
    return encoded
