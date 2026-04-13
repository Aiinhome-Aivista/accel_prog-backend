# from config import get_db_connection
# from flask import jsonify, request


# def complete_subtopic_module_course_wise_by_user():

#     data = request.get_json() or {}

#     user_id = data.get("user_id")
#     course_id = data.get("course_id")
#     module_id = data.get("module_id")
#     subtopic_id = data.get("subtopic_id")

#     if not user_id or not course_id or not module_id or not subtopic_id:
#         return jsonify({
#             "error": "user_id, course_id, module_id and subtopic_id are required"
#         }), 400

#     conn = None
#     cur = None

#     try:

#         conn = get_db_connection()
#         cur = conn.cursor()

#         cur.execute(
#             "CALL course.complete_subtopic_and_progress_update(%s,%s,%s,%s,%s)",
#             (user_id, course_id, module_id, subtopic_id, None)
#         )

#         row = cur.fetchone()

#         if row is None:
#             result = {"message": "Subtopic completed successfully"}
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


@log_api("complete_subtopic_module_course_wise_by_user")   # decorator add
def complete_subtopic_module_course_wise_by_user():

    data = request.get_json() or {}

    user_id = data.get("user_id")
    course_id = data.get("course_id")
    module_id = data.get("module_id")
    subtopic_id = data.get("subtopic_id")

    if not user_id or not course_id or not module_id or not subtopic_id:
        return jsonify({
            "error": "user_id, course_id, module_id and subtopic_id are required"
        }), 400

    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "CALL course.complete_subtopic_and_progress_update(%s,%s,%s,%s,%s)",
            (user_id, course_id, module_id, subtopic_id, None)
        )

        row = cur.fetchone()

        if row is None:
            result = {"message": "Subtopic completed successfully"}
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