# from flask import request
# from config import get_db_connection
# from utils.jwt_helper import generate_jwt



# def login():
#     data = request.json
#     email = data["email"]
#     password = data["password"]

#     conn = get_db_connection()
#     cur = conn.cursor()

#     # call procedure
#     cur.callproc("login_user_proc", [email, password, None, None, None])

#     result = cur.fetchone()

#     if not result or result[0] is None:
#         return {"error": "Invalid credentials"}, 401

#     user_id, is_verified, is_completed = result

#     if not is_verified:
#         return {"error": "Email not verified"}, 403

#     # JWT
#     token = generate_jwt(user_id)

#     next_step = "dashboard" if is_completed else "questionnaire"

#     return {"token": token, "next_step": next_step}




# from flask import request
# from config import get_db_connection
# from utils.jwt_helper import generate_jwt



# def login():
#     data = request.json
#     email = data["email"]
#     password = data["password"]

#     conn = get_db_connection()
#     cur = conn.cursor()

#     # call procedure
#     cur.callproc("login_user_proc", [email, password, None, None, None])

#     result = cur.fetchone()

#     if not result or result[0] is None:
#         return {"error": "Invalid credentials"}, 401

#     user_id, is_verified, is_completed = result

#     if not is_verified:
#         return {"error": "Email not verified"}, 403

#     # JWT
#     token = generate_jwt(user_id)

#     next_step = "dashboard" if is_completed else "questionnaire"

#     return {"token": token, "next_step": next_step}



from flask import request
from config import get_db_connection
from utils.jwt_helper import generate_jwt
from utils.logging_service import log_api


@log_api("login")
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    conn = get_db_connection()
    cur = conn.cursor()

    # call procedure
    cur.callproc("login_user_proc", [email, password, None, None, None])

    result = cur.fetchone()

    if not result or result[0] is None:
        return {"error": "Invalid credentials"}, 401

    user_id, is_verified, is_completed = result

    if not is_verified:
        return {"error": "Email not verified"}, 403

    # JWT
    token = generate_jwt(user_id)

    next_step = "dashboard" if is_completed else "questionnaire"

    return {"token": token, "next_step": next_step}