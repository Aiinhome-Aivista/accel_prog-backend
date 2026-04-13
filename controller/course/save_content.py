# from flask import request, jsonify
# from config import get_db_connection
# import psycopg2.extras


# def save_content():
#     data = request.json

#     #  Extract fields
#     course_id = data.get("course_id")
#     module_id = data.get("module_id")
#     subtopic_id = data.get("subtopic_id")
#     content_type = data.get("subtopic_type")
#     content = data.get("content")
#     user_id = data.get("created_by")   # UI theke asche

#     #  Validation
#     if not all([course_id, module_id, subtopic_id, content_type, content, user_id]):
#         return jsonify({
#             "status": "error",
#             "message": "All fields are required"
#         }), 400

#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

#     try:
#         #  CALL stored procedure
#         cursor.execute(
#             "CALL course.save_content(%s, %s, %s, %s, %s::JSONB, %s, %s::JSONB);",
#             (
#                 course_id,
#                 module_id,
#                 subtopic_id,
#                 content_type,
#                 psycopg2.extras.Json(content),  #  important for JSON
#                 user_id,
#                 None
#             )
#         )

#         row = cursor.fetchone()

#         #  Handle empty response
#         if not row or not row.get("p_result"):
#             return jsonify({
#                 "status": "error",
#                 "message": "No response from procedure"
#             }), 500

#         return jsonify(row["p_result"]), 200

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


@log_api("save_content")   # ✅ decorator add
def save_content():
    data = request.json

    #  Extract fields
    course_id = data.get("course_id")
    module_id = data.get("module_id")
    subtopic_id = data.get("subtopic_id")
    content_type = data.get("subtopic_type")
    content = data.get("content")
    user_id = data.get("created_by")   # UI theke asche

    #  Validation
    if not all([course_id, module_id, subtopic_id, content_type, content, user_id]):
        return jsonify({
            "status": "error",
            "message": "All fields are required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        #  CALL stored procedure
        cursor.execute(
            "CALL course.save_content(%s, %s, %s, %s, %s::JSONB, %s, %s::JSONB);",
            (
                course_id,
                module_id,
                subtopic_id,
                content_type,
                psycopg2.extras.Json(content),  #  important for JSON
                user_id,
                None
            )
        )

        row = cursor.fetchone()

        #  Handle empty response
        if not row or not row.get("p_result"):
            return jsonify({
                "status": "error",
                "message": "No response from procedure"
            }), 500

        return jsonify(row["p_result"]), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()