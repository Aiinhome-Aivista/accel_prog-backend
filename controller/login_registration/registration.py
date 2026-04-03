from flask import request
from config import get_db_connection
from psycopg2.extras import Json, RealDictCursor


def register():
    conn = None
    try:
        # =========================
        # 📥 GET REQUEST BODY
        # =========================
        data = request.get_json()

        if not data:
            return {
                "status": "error",
                "message": "Invalid request body"
            }, 400

        # =========================
        # 🛢 DB CONNECTION
        # =========================
        conn = get_db_connection()
        conn.autocommit = False   # 🔥 IMPORTANT
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cursor_name = "reg_cursor"

        # =========================
        # 🚀 BEGIN TRANSACTION
        # =========================
        cur.execute("BEGIN;")

        # =========================
        # 📞 CALL PROCEDURE
        # =========================
        cur.execute("""
            CALL registration.insert_registration_proc(%s, %s, %s, %s, %s)
        """, (Json(data), 0, "", 0, cursor_name))

        # =========================
        # 📤 FETCH RESULT
        # =========================
        cur.execute(f'FETCH ALL FROM "{cursor_name}";')
        result = cur.fetchone()

        # cursor close (good practice)
        cur.execute(f'CLOSE "{cursor_name}";')

        # =========================
        # 💾 COMMIT
        # =========================
        conn.commit()

        print("RESULT:", result)

        # =========================
        #  NO RESULT
        # =========================
        if not result:
            return {
                "status": "error",
                "message": "No response from procedure"
            }, 500

        # =========================
        # ✅ EXTRACT VALUES
        # =========================
        status = result.get("o_status")
        message = result.get("o_message")
        user_id = result.get("o_user_id")

        # =========================
        # 📤 RESPONSE HANDLE
        # =========================
        if status == 201:
            return {
                "status": "success",
                "message": message,
                "user_id": user_id
            }, 201

        elif status == 409:
            return {
                "status": "error",
                "message": message
            }, 409

        else:
            return {
                "status": "error",
                "message": message or "Something went wrong"
            }, 500

    except Exception as e:
        if conn:
            conn.rollback()

        print("REAL ERROR:", repr(e))

        return {
            "status": "error",
            "message": "Internal Server Error",
            "error": str(e)
        }, 500

    finally:
        if conn:
            conn.close()