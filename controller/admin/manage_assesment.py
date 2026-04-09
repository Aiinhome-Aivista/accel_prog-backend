from flask import request, jsonify
from config import get_db_connection
import psycopg2.extras


def manage_assessment_questions():
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute(
            """CALL course.manage_assessment_questions(
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            );""",
            (
                data.get("action"),
                data.get("question_id"),
                data.get("course_id"),
                data.get("module_id"),
                data.get("subtopic_id"),
                data.get("category_id"),
                data.get("type_id"),
                data.get("question_text"),
                data.get("options"),
                data.get("correct_answer"),
                data.get("marks"),
                data.get("order_no"),
                None,
            ),
        )

        row = cursor.fetchone()

        return jsonify(row["p_result"]), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
