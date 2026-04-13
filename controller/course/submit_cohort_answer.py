# from flask import request, jsonify
# from config import get_db_connection
# import psycopg2.extras


# def submit_cohort_answer():
#     data = request.json

#     user_id = data.get("user_id")
#     course_id = data.get("course_id")
#     module_id = data.get("module_id")
#     subtopic_id = data.get("subtopic_id")
#     cohort_question_id = data.get("cohort_question_id")
#     answer = data.get("answer")

#     # Validation
#     if not all([user_id, course_id, module_id, subtopic_id, cohort_question_id, answer]):
#         return jsonify({
#             "status": "error",
#             "message": "All fields are required"
#         }), 400

#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

#     try:
#         # CALL procedure
#         cursor.execute(
#             "CALL course.submit_cohort_answer(%s,%s,%s,%s,%s,%s,%s);",
#             (
#                 user_id,
#                 course_id,
#                 module_id,
#                 subtopic_id,
#                 cohort_question_id,
#                 answer,
#                 None
#             )
#         )

#         # IMPORTANT
#         row = cursor.fetchone()

#         if not row or not row.get("result"):
#             return jsonify({
#                 "status": "error",
#                 "message": "No response from procedure"
#             }), 500

#         return jsonify(row["result"]), 200

#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

#     finally:
#         cursor.close()
#         conn.close()




from flask import request, jsonify
from config import get_db_connection
import psycopg2.extras
from utils.logging_service import log_api   # ✅ import add


@log_api("submit_cohort_answer")   # ✅ decorator add
def submit_cohort_answer():
    data = request.json

    user_id = data.get("user_id")
    course_id = data.get("course_id")
    module_id = data.get("module_id")
    subtopic_id = data.get("subtopic_id")
    cohort_question_id = data.get("cohort_question_id")
    answer = data.get("answer")

    # Validation
    if not all([user_id, course_id, module_id, subtopic_id, cohort_question_id, answer]):
        return jsonify({
            "status": "error",
            "message": "All fields are required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # CALL procedure
        cursor.execute(
            "CALL course.submit_cohort_answer(%s,%s,%s,%s,%s,%s,%s);",
            (
                user_id,
                course_id,
                module_id,
                subtopic_id,
                cohort_question_id,
                answer,
                None
            )
        )

        # IMPORTANT
        row = cursor.fetchone()

        if not row or not row.get("result"):
            return jsonify({
                "status": "error",
                "message": "No response from procedure"
            }), 500

        return jsonify(row["result"]), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()