# from config import get_db_connection
# from flask import jsonify, request


# from psycopg2.extras import RealDictCursor


# def verify_otp_service():
#     data = request.get_json() or {}
#     email = data.get("email")
#     otp = data.get("otp") or data.get("otp_code")

#     if not email or not otp:
#         return (
#             jsonify({"status": "error", "message": "email and otp are required"}),
#             400,
#         )

#     conn = None
#     try:
#         conn = get_db_connection()
#         # RealDictCursor ব্যবহার করলে row['p_result'] সরাসরি পাওয়া যাবে
#         cur = conn.cursor(cursor_factory=RealDictCursor)

#         cur.execute("CALL login.verify_otp_sp_v2(%s, %s, %s)", (email, otp, None))
#         row = cur.fetchone()
#         conn.commit()

#         if row and "p_result" in row:
#             result = row["p_result"]
#             # যদি স্ট্যাটাস সাকসেস হয় তবে ২০০, নয়তো ৪০০ বা ৫০০ পাঠানো ভালো
#             status_code = 200 if result.get("status") == "success" else 400
#             return jsonify(result), status_code

#         return jsonify({"status": "error", "message": "No response from database"}), 500

#     except Exception as e:
#         if conn:
#             conn.rollback()
#         return jsonify({"status": "error", "message": str(e)}), 500
#     finally:
#         if conn:
#             conn.close()





from config import get_db_connection
from flask import jsonify, request
from psycopg2.extras import RealDictCursor
from utils.logging_service import log_api


@log_api("verify-otp")
def verify_otp_service():
    data = request.get_json() or {}
    email = data.get("email")
    otp = data.get("otp") or data.get("otp_code")

    if not email or not otp:
        return (
            jsonify({"status": "error", "message": "email and otp are required"}),
            400,
        )

    conn = None

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            "CALL login.verify_otp_sp_v2(%s, %s, %s)",
            (email, otp, None),
        )

        row = cur.fetchone()
        conn.commit()

        if row and "p_result" in row:
            result = row["p_result"]
            status_code = 200 if result.get("status") == "success" else 400
            return jsonify(result), status_code

        return jsonify({"status": "error", "message": "No response from database"}), 500

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if conn:
            conn.close()