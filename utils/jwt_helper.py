import utils.jwt_helper as jwt_helper
from datetime import datetime, timedelta
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRY_HOURS


def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
        "iat": datetime.utcnow(),
    }

    token = jwt_helper.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt(token):
    try:
        decoded = jwt_helper.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded["user_id"], None
    except jwt_helper.ExpiredSignatureError:
        return None, "Token expired"
    except jwt_helper.InvalidTokenError:
        return None, "Invalid token"


def get_user_from_token(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        token = auth_header.split(" ")[1]  # Bearer <token>
        user_id, error = verify_jwt(token)

        if error:
            return None

        return user_id

    except:
        return None
