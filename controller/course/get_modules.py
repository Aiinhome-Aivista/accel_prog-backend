# import json
# from config import get_db_connection
# from flask import jsonify, request


# def get_modules_dashboard_service():
#     conn = None
#     cur = None
#     data = request.get_json() or {}

#     course_id = data.get("course_id")
#     user_id = data.get("user_id")

#     if not course_id:
#         return jsonify({"status": "error", "message": "course_id is required"}), 400

#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()

#         cur.execute("BEGIN")

#         cur.execute(
#             "CALL course.get_modules_with_days_v4(%s, %s, %s)",
#             (course_id, user_id, 'mycursor')
#         )

#         cur.execute("FETCH ALL FROM mycursor")
#         rows = cur.fetchall()

#         # print("DEBUG:", rows)

#         result = []
#         if rows:
#             first_row = rows[0]
#             if isinstance(first_row, dict):
#                 result = first_row.get("v_result") or first_row.get("?column?") or []
#             else:
#                 result = first_row[0]

#         if isinstance(result, str):
#             try:
#                 result = json.loads(result)
#             except json.JSONDecodeError:
#                 pass

#         # 🔥 FIX HERE
#         conn.rollback()   # ✅ NOT commit

#         return jsonify({
#             "status": "success",
#             "data": result
#         }), 200

#     except Exception as e:
#         print("ERROR:", str(e))
#         return jsonify({"status": "error", "message": str(e)}), 500

#     finally:
#         if cur:
#             cur.close()
#         if conn:
#             conn.close()




import json
from config import get_db_connection
from flask import jsonify, request
from utils.logging_service import log_api   # ✅ import add


@log_api("get_modules_dashboard")   # ✅ decorator add
def get_modules_dashboard_service():
    conn = None
    cur = None
    data = request.get_json() or {}

    course_id = data.get("course_id")
    user_id = data.get("user_id")

    if not course_id:
        return jsonify({"status": "error", "message": "course_id is required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("BEGIN")

        cur.execute(
            "CALL course.get_modules_with_days_v4(%s, %s, %s)",
            (course_id, user_id, 'mycursor')
        )

        cur.execute("FETCH ALL FROM mycursor")
        rows = cur.fetchall()

        result = []
        if rows:
            first_row = rows[0]
            if isinstance(first_row, dict):
                result = first_row.get("v_result") or first_row.get("?column?") or []
            else:
                result = first_row[0]

        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                pass

        # 🔥 FIX HERE
        conn.rollback()   # ✅ NOT commit

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()