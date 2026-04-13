from flask import request
from config import get_db_connection
from psycopg2.extras import Json, RealDictCursor


def register():
    conn = None
    try:
        # =========================
        #  GET REQUEST BODY
        # =========================
        data = request.get_json()

        if not data:
            return {"status": "error", "message": "Invalid request body"}, 400

        # =========================
        # 🛢 DB CONNECTION
        # =========================
        conn = get_db_connection()
        conn.autocommit = False
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # =========================
        #  CALL PROCEDURE
        # =========================
    
        cur.execute(
            "CALL registration.insert_registration_proc_v3(%s, %s, %s, %s, %s)",
            (Json(data), 0, "", 0, "reg_cursor"),
        )

        # =========================
        #  FETCH FROM REFCURSOR
        # =========================
        cur.execute('FETCH ALL FROM "reg_cursor";')
        result = cur.fetchone()

        cur.execute('CLOSE "reg_cursor";')
        conn.commit()

        if not result:
            return {"status": "error", "message": "No response from procedure"}, 500

        # =========================
        #  DIRECT RESPONSE FROM SP
        # =========================

        status_code = result.get("status_code", 200) 

        return result, status_code

    except Exception as e:
        if conn:
            conn.rollback()
        print("REGISTRATION ERROR:", repr(e))
        return {
            "status": "error",
            "message": "Internal Server Error",
            "error": str(e),
        }, 500

    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()    
