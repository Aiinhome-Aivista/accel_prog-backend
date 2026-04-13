# from config import get_db_connection
# from flask import jsonify, request


# def enroll_user():

#     data = request.get_json() or {}

#     user_id = data.get("user_id")
#     course_id = data.get("course_id")
#     role_id = data.get("role_id")

#     if not user_id or not course_id or not role_id:
#         return jsonify({
#             "error": "user_id, course_id and role_id are required"
#         }), 400

#     conn = None
#     cur = None

#     try:

#         conn = get_db_connection()
#         cur = conn.cursor()

#         cur.execute(
#             "CALL course.enroll_user_in_course(%s,%s,%s,%s)",
#             (user_id, course_id, role_id, None)
#         )

#         row = cur.fetchone()

#         if row is None:
#             result = {"message": "Enrollment completed"}
#         elif isinstance(row, dict):
#             first_key = next(iter(row), None)
#             result = row[first_key] if first_key else row
#         else:
#             result = row[0]

#         conn.commit()

#         return jsonify(result), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

#     finally:
#         if cur:
#             cur.close()
#         if conn:
#             conn.close()




from config import get_db_connection
from flask import jsonify, request
from utils.logging_service import log_api   # import add


@log_api("course_enrollment")   # decorator add
def enroll_user():

    data = request.get_json() or {}

    user_id = data.get("user_id")
    course_id = data.get("course_id")
    role_id = data.get("role_id")

    if not user_id or not course_id or not role_id:
        return jsonify({
            "error": "user_id, course_id and role_id are required"
        }), 400

    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "CALL course.enroll_user_in_course(%s,%s,%s,%s)",
            (user_id, course_id, role_id, None)
        )

        row = cur.fetchone()

        if row is None:
            result = {"message": "Enrollment completed"}
        elif isinstance(row, dict):
            first_key = next(iter(row), None)
            result = row[first_key] if first_key else row
        else:
            result = row[0]

        conn.commit()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()