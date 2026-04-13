# from config import get_db_connection
# from flask import request
# from utils.email_helper import send_otp_email
# from utils.response_helper import error_response, success_response
# import json


# def send_otp_service():
#     data = request.get_json() or {}
#     email = data.get("email")
#     if not email:
#         return error_response("email is required", 400)

#     conn = None
#     cur = None
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()

#         cur.execute("CALL login.generate_and_insert_otp_sp(%s, %s)", (email, None))
#         row = cur.fetchone()

#         if row is None:
#             return error_response("OTP generation failed", 500)
#         elif isinstance(row, dict):
#             first_key = next(iter(row), None)
#             result = row[first_key] if first_key is not None else row
#         else:
#             result = row[0]

#         if isinstance(result, str):
#             result = json.loads(result)

#         otp_code = None
#         if isinstance(result, dict):
#             otp_code = (result.get("data") or {}).get("otp_code")

#         if not otp_code:
#             return error_response("OTP not found in procedure response", 500)

#         send_otp_email(email, otp_code)

#         conn.commit()
#         return success_response("OTP sent successfully", 200)
#     except Exception as e:
#         return error_response(str(e), 500)
#     finally:
#         if cur:
#             cur.close()
#         if conn:
#             conn.close()




from config import get_db_connection
from flask import request
from utils.email_helper import send_otp_email
from utils.response_helper import error_response, success_response
from utils.logging_service import log_api
import json


@log_api("send-otp")
def send_otp_service():
    data = request.get_json() or {}
    email = data.get("email")

    if not email:
        return error_response("email is required", 400)

    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("CALL login.generate_and_insert_otp_sp(%s, %s)", (email, None))
        row = cur.fetchone()

        if row is None:
            return error_response("OTP generation failed", 500)

        elif isinstance(row, dict):
            first_key = next(iter(row), None)
            result = row[first_key] if first_key is not None else row
        else:
            result = row[0]

        if isinstance(result, str):
            result = json.loads(result)

        otp_code = None
        if isinstance(result, dict):
            otp_code = (result.get("data") or {}).get("otp_code")

        if not otp_code:
            return error_response("OTP not found in procedure response", 500)

        send_otp_email(email, otp_code)

        conn.commit()

        return success_response("OTP sent successfully", 200)

    except Exception as e:
        return error_response(str(e), 500)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()