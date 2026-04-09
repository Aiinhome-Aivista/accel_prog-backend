from flask import request, jsonify
from config import get_db_connection


def submit_user_answer():

    data = request.get_json()

    # =============================
    # STEP 1: Validate Payload
    # =============================
    required_fields = [
        "user_id",
        "course_id",
        "module_id",
        "subtopic_id",
        "question_id",
        "user_answer"
    ]

    missing_fields = [f for f in required_fields if f not in data]

    if missing_fields:
        return jsonify({
            "status": "error",
            "message": f"Missing fields: {', '.join(missing_fields)}"
        }), 400

    # =============================
    # STEP 2: Extract Values
    # =============================
    user_id = data["user_id"]
    course_id = data["course_id"]
    module_id = data["module_id"]
    subtopic_id = data["subtopic_id"]
    question_id = data["question_id"]
    user_answer = data["user_answer"]
    time_taken = data.get("time_taken", 0)

    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # =============================
        # STEP 3: CALL STORED PROCEDURE
        # =============================
        cur.execute(
            "CALL course.submit_user_answer(%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                user_id,
                course_id,
                module_id,
                subtopic_id,
                question_id,
                user_answer,
                time_taken,
                None
            )
        )

        row = cur.fetchone()

        # =============================
        # STEP 4: Handle Response
        # =============================
        if row is None:
            result = {"status": "success"}
        elif isinstance(row, dict):
            key = next(iter(row))
            result = row[key]
        else:
            result = row[0]

        conn.commit()

        return jsonify(result), 200

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