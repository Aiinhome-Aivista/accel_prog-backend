# from config import get_db_connection
# from flask import jsonify


# def get_courses_dashboard_service():
#     conn = None
#     cur = None

#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()

        
#         cur.execute("CALL course.get_all_courses_dashboard(%s)", (None,))

#         row = cur.fetchone()

#         if row is None:
#             result = []
#         elif isinstance(row, dict):
#             first_key = next(iter(row), None)
#             result = row[first_key] if first_key is not None else row
#         else:
#             result = row[0]

#         conn.commit()

#         return jsonify({"status": "success", "data": result}), 200

#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

#     finally:
#         if cur:
#             cur.close()
#         if conn:
#             conn.close()



from config import get_db_connection
from flask import jsonify, request


def get_courses_dashboard_service():
    conn = None
    cur = None

    try:
        #  args theke user_id nebo
        user_id = request.args.get("user_id", type=int)

        if not user_id:
            return jsonify({
                "status": "fail",
                "message": "user_id is required",
                "data": []
            }), 400

        conn = get_db_connection()
        cur = conn.cursor()

        #  updated CALL (IN + OUT)
        cur.execute(
            "CALL course.get_all_courses_dashboard_v1(%s, %s)",
            (user_id, None)
        )

        row = cur.fetchone()

        if row is None:
            result = []
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