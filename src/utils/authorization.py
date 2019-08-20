import jwt
from datetime import datetime, timedelta

def encode(data):
    payload = {
        "data":data,
        "exp":datetime.utcnow() + timedelta(seconds=10),
        "iat":datetime.utcnow()
    }

    encoded = jwt.encode(payload, "sate-kelinci", algorithm="HS256").decode('utf-8')
    return encoded

def decode(data):
    decoded = jwt.decode(data, "sate-kelinci", algorithms=['HS256'])
    return decoded