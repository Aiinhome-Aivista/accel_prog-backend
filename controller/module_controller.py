from config import get_db_connection


def add_module(data):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL usp_add_module(%s, %s, %s, %s)",
        (
            data["course_id"],
            data["module_name"],
            data.get("module_description"),
            data.get("module_order"),
        ),
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Module added"}
