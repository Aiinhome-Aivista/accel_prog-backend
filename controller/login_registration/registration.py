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
            return {"status": "error", "message": "Invalid request body"}, 400

        # =========================
        # 🛢 DB CONNECTION
        # =========================
        conn = get_db_connection()
        conn.autocommit = False
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # =========================
        # 📞 CALL PROCEDURE
        # =========================
        # v3 অনুযায়ী প্যারামিটার: (json, status, message, user_id, cursor)
        # এখানে %s গুলোর জন্য আর্গুমেন্ট পাস করা হচ্ছে
        cur.execute(
            "CALL registration.insert_registration_proc_v3(%s, %s, %s, %s, %s)",
            (Json(data), 0, "", 0, "reg_cursor"),
        )

        # =========================
        # 📤 FETCH FROM REFCURSOR
        # =========================
        # প্রোসিডিউর এর ভেতরে থাকা 'ref' কার্সার থেকে ডাটা রিড করা
        cur.execute('FETCH ALL FROM "reg_cursor";')
        result = cur.fetchone()

        cur.execute('CLOSE "reg_cursor";')
        conn.commit()

        if not result:
            return {"status": "error", "message": "No response from procedure"}, 500

        # =========================
        # ✅ DIRECT RESPONSE FROM SP
        # =========================
        # প্রোসিডিউরের SELECT স্টেটমেন্টে যে নামগুলো (alias) দিয়েছেন, এখানে সেগুলোই আসবে।
        # আপনার SP অনুযায়ী: status, message, user_id, full_name, role_id, access_control

        status_code = result.get("status", 200)  # SP থেকে আসা স্ট্যাটাস কোড

        # আপনি চেয়েছেন এপিআই রেসপন্স মডিফাই না করে সরাসরি SP রেসপন্স দেখাতে
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
