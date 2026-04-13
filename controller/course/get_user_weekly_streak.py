# from config import get_db_connection
# from flask import jsonify, request


# def get_user_weekly_streak():

#     data = request.get_json() or {}

#     user_id = data.get("user_id")

#     #  Validation
#     if not user_id:
#         return jsonify({"error": "user_id is required"}), 400

#     conn = None
#     cur = None

#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()

#         # CALL stored procedure
#         cur.execute(
#             "CALL login.get_user_weekly_streak(%s, %s)",
#             (user_id, None)
#         )

#         row = cur.fetchone()

#         #  Same response handling pattern
#         if row is None:
#             result = {
#                 "streak_days": 0,
#                 "weekly": []
#             }

#         elif isinstance(row, dict):
#             first_key = next(iter(row), None)
#             result = row[first_key] if first_key is not None else row

#         else:
#             result = row[0]

#         conn.commit()

#         return jsonify({
#             "status": "success",
#             "data": result
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

#     finally:
#         if cur:
#             cur.close()
#         if conn:
#             conn.close()




from config import get_db_connection
from flask import jsonify, request
from utils.logging_service import log_api   # import add


@log_api("get_user_weekly_streak")   #  decorator add
def get_user_weekly_streak():

    data = request.get_json() or {}

    user_id = data.get("user_id")

    #  Validation
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # CALL stored procedure
        cur.execute(
            "CALL login.get_user_weekly_streak(%s, %s)",
            (user_id, None)
        )

        row = cur.fetchone()

        #  Same response handling pattern
        if row is None:
            result = {
                "streak_days": 0,
                "weekly": []
            }

        elif isinstance(row, dict):
            first_key = next(iter(row), None)
            result = row[first_key] if first_key is not None else row

        else:
            result = row[0]

        conn.commit()

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()