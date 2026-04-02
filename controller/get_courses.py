from flask import jsonify
from config import get_db_connection

def get_program_courses():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("CALL course.usp_get_program_with_courses(%s)", (None,))

    # PostgreSQL procedure output fetch trick
    cursor.execute('FETCH ALL IN "<unnamed portal 1>"')  # optional depending driver

    # Better approach:
    cursor.execute(
        """
        DO $$
        DECLARE v_result JSON;
        BEGIN
            CALL course.usp_get_program_with_courses(v_result);
            RAISE NOTICE '%', v_result;
        END $$;
    """
    )

    # Real-world → better use FUNCTION instead 😄

    cursor.close()
    conn.close()

    return jsonify(
        {
            "success": True,
            "message": "Procedure executed (use FUNCTION for cleaner fetch)",
        }
    )
