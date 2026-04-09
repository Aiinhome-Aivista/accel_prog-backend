from flask import jsonify
from config import get_db_connection
import psycopg2.extras


def get_assessment_questions_v2():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cursor.execute(
            "CALL course.get_assessment_questions_full_v2(%s::JSONB);", (None,)
        )

        row = cursor.fetchone()

        if not row or not row.get("p_result"):
            return jsonify({"status": "error", "message": "No data found"}), 404

        return jsonify(row["p_result"]), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
