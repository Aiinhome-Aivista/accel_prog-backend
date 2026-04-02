from config import get_db_connection
from flask import jsonify, request


def send_otp_service():
    data = request.get_json() or {}
    email = data.get("email")
    if not email:
        return jsonify({"error": "email is required"}), 400

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("CALL login.generate_and_insert_otp_sp(%s, %s)", (email, None))
        row = cur.fetchone()

        if row is None:
            result = {"message": "OTP sent"}
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
