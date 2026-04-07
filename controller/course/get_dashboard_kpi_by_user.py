from config import get_db_connection
from flask import jsonify, request


def get_dashboard_kpi_by_user():
    data = request.get_json() or {}

    user_id = data.get("user_id")

    # 🔥 Validation
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # CALL stored procedure
        cur.execute(
            "CALL login.get_dashboard_kpi_by_user_id(%s, %s)",
            (user_id, None)
        )

        row = cur.fetchone()

        # 🔥 Same response handling as google_signin
        if row is None:
            result = {
                "in_progress_count": 0,
                "completed_count": 0,
                "streak_days": 0,
                "overall_progress": 0
            }

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
        return jsonify({"error": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()