# from config import get_db_connection
# from flask import jsonify, request


# def google_signin():
#     data = request.get_json() or {}

#     email = data.get("email")
#     full_name = data.get("full_name")
#     is_google_verified = data.get("is_google_verified", False)

#     # Validation
#     if not email or not full_name:
#         return jsonify({"error": "email and full_name are required"}), 400

#     conn = None
#     cur = None

#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()

#         # Call stored procedure
#         cur.execute(
#             "CALL login.google_signin_sp_v5(%s, %s, %s, %s)",
#             (email, full_name, is_google_verified, None)
#         )

#         row = cur.fetchone()

#         # Handle response (same pattern as your OTP API)
#         if row is None:
#             result = {"message": "Google Sign-In successful"}
#         elif isinstance(row, dict):
#             first_key = next(iter(row), None)
#             result = row[first_key] if first_key is not None else row
#         else:
#             result = row[0]

#         conn.commit()
#         return result, 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

#     finally:
#         if cur:
#             cur.close()
#         if conn:
#             conn.close()





from config import get_db_connection
from flask import jsonify, request
from utils.logging_service import log_api


@log_api("google-signin")
def google_signin():
    data = request.get_json() or {}

    email = data.get("email")
    full_name = data.get("full_name")
    is_google_verified = data.get("is_google_verified", False)

    # Validation
    if not email or not full_name:
        return jsonify({"error": "email and full_name are required"}), 400

    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Call stored procedure
        cur.execute(
            "CALL login.google_signin_sp_v5(%s, %s, %s, %s)",
            (email, full_name, is_google_verified, None)
        )

        row = cur.fetchone()

        # Handle response
        if row is None:
            result = {"message": "Google Sign-In successful"}
        elif isinstance(row, dict):
            first_key = next(iter(row), None)
            result = row[first_key] if first_key is not None else row
        else:
            result = row[0]

        conn.commit()
        return result, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()