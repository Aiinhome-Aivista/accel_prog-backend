from flask import request
from config import get_db_connection
from psycopg2.extras import Json, RealDictCursor


def register():
    conn = None
    try:
        data = request.get_json()
        if not data:
            return {"status": "error", "message": "Invalid request body"}, 400

        conn = get_db_connection()
        # Autocommit True রাখলে BEGIN/COMMIT ম্যানুয়ালি করতে হয় না,
        # তবে প্রোসিডিউরের ভেতর ট্রানজেকশন থাকলে এটা এভাবেই রাখুন
        conn.autocommit = False
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # =========================
        # 📞 CALL PROCEDURE (Fixed Arguments)
        # =========================
        # আপনার প্রোসিডিউরে শুধু ২টো প্যারামিটার: ১টি ইনপুট (JSON), ১টি ইন-আউট (result)
        cur.execute(
            "CALL registration.insert_registration_proc_v3(%s, %s)", (Json(data), None)
        )

        # INOUT প্যারামিটারের ভ্যালু সরাসরি fetch করলেই পাওয়া যায়
        raw_result = cur.fetchone()

        # PostgreSQL CALL রিটার্ন করে প্যারামিটারের নাম দিয়ে (p_result)
        db_response = raw_result.get("p_result") if raw_result else None

        conn.commit()

        if not db_response:
            return {"status": "error", "message": "No response from database"}, 500

        # =========================
        # ✅ EXTRACT VALUES (Based on your SQL JSON structure)
        # =========================
        status_code = db_response.get("status_code", 500)
        message = db_response.get("message")
        user_data = db_response.get("user", {})

        return {
            "status": db_response.get("status"),
            "message": message,
            "user_id": user_data.get("user_id"),
            "full_name": user_data.get("full_name"),
            "role_id": user_data.get("role_id"),
            "meta": db_response.get("meta"),
        }, status_code

    except Exception as e:
        if conn:
            conn.rollback()
        print("REAL ERROR:", repr(e))
        return {
            "status": "error",
            "message": "Internal Server Error",
            "error": str(e),
        }, 500

    finally:
        if conn:
            conn.close()
