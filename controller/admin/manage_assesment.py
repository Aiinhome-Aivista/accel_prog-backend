import json

from flask import request, jsonify
from config import get_db_connection
import psycopg2.extras


def manage_assessment_questions():
    payload = request.get_json(silent=True)
    if isinstance(payload, list):
        payload = payload[0] if payload else {}
    if not isinstance(payload, dict):
        payload = {}

    if not payload.get("action"):
        return jsonify({"status": "error", "message": "action is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        options_value = payload.get("options")
        correct_answer_value = payload.get("correct_answer")

        # Allow client to send JSON as string too.
        if isinstance(options_value, str):
            try:
                options_value = json.loads(options_value)
            except json.JSONDecodeError:
                pass
        if isinstance(correct_answer_value, str):
            try:
                correct_answer_value = json.loads(correct_answer_value)
            except json.JSONDecodeError:
                pass

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
                payload.get("action"),
                payload.get("question_id"),
                payload.get("course_id"),
                payload.get("module_id"),
                payload.get("subtopic_id"),
                payload.get("category_id"),
                payload.get("type_id"),
                payload.get("question_text"),
                options_value,
                correct_answer_value,
                payload.get("marks"),
                payload.get("order_no"),
                None,
            ),
        )

        row = cursor.fetchone()

        if not row:
            return (
                jsonify({"status": "error", "message": "No response from procedure"}),
                500,
            )

        result = row.get("p_result") or row.get("result")
        if result is None:
            first_key = next(iter(row), None)
            result = row[first_key] if first_key is not None else None

        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                pass

        if result is None:
            return (
                jsonify(
                    {"status": "error", "message": "Procedure returned empty result"}
                ),
                500,
            )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
