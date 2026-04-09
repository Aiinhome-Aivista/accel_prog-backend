import json
from flask import request, jsonify
from config import get_db_connection
import psycopg2.extras


def manage_assessment_questions():
    payload = request.get_json(silent=True)

    if not payload:
        return jsonify({"status": "error", "message": "Invalid payload"}), 400

    # detect batch or single
    is_batch_request = False
    if isinstance(payload, dict) and "questions" in payload:
        is_batch_request = True
        questions = payload.get("questions", [])
    elif isinstance(payload, list):
        is_batch_request = True
        questions = payload
    else:
        questions = [payload]

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    results = []

    try:
        for q in questions:

            if not q.get("action"):
                return (
                    jsonify({"status": "error", "message": "action is required"}),
                    400,
                )

            options_value = q.get("options")
            correct_answer_value = q.get("correct_answer")

            # string → JSON
            if isinstance(options_value, str):
                try:
                    options_value = json.loads(options_value)
                except:
                    pass

            if isinstance(correct_answer_value, str):
                try:
                    correct_answer_value = json.loads(correct_answer_value)
                except:
                    pass

            # wrap JSONB
            if isinstance(options_value, (dict, list)):
                options_value = psycopg2.extras.Json(options_value)

            if isinstance(correct_answer_value, (dict, list)):
                correct_answer_value = psycopg2.extras.Json(correct_answer_value)

            cursor.execute(
                """CALL admin.manage_assessment_questions(
        %s::TEXT,
        %s::BIGINT,
        %s::INT,
        %s::INT,
        %s::INT,
        %s::INT,
        %s::INT,
        %s::TEXT,
        %s::JSONB,
        %s::JSONB,
        %s::INT,
        %s::INT,
        %s::JSONB
    );""",
                (
                    q.get("action"),
                    q.get("question_id") if q.get("question_id") is not None else None,
                    q.get("course_id") if q.get("course_id") is not None else None,
                    q.get("module_id") if q.get("module_id") is not None else None,
                    q.get("subtopic_id") if q.get("subtopic_id") is not None else None,
                    q.get("category_id") if q.get("category_id") is not None else None,
                    q.get("type_id") if q.get("type_id") is not None else None,
                    q.get("question_text"),
                    options_value,
                    correct_answer_value,
                    q.get("marks") if q.get("marks") is not None else None,
                    q.get("order_no") if q.get("order_no") is not None else None,
                    None,
                ),
            )

            row = cursor.fetchone()

            if not row:
                continue

            result = row.get("p_result") or row.get("result")

            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except:
                    pass

            results.append(result)

        if not is_batch_request and len(results) == 1:
            return jsonify({"status": "success", "data": results[0]}), 200

        return jsonify({"status": "success", "data": results}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
