from datetime import datetime

from app.database import get_connection


def row_to_dict(row):
    if row is None:
        return None

    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "priority": row["priority"],
        "completed": bool(row["completed"]),
        "due_date": row["due_date"],
        "created_at": row["created_at"],
    }


def create_task(title, description, priority, due_date):
    connection = get_connection()

    created_at = datetime.now().isoformat()

    cursor = connection.execute(
        """
        INSERT INTO tasks
        (title, description, priority, due_date, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            priority,
            due_date,
            created_at,
        ),
    )

    connection.commit()

    task_id = cursor.lastrowid

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    connection.close()

    return row_to_dict(row)


def get_all_tasks():
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM tasks ORDER BY id"
    ).fetchall()

    connection.close()

    return [row_to_dict(row) for row in rows]


def get_task(task_id):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    connection.close()

    return row_to_dict(row)


def update_task(task_id, updates):
    connection = get_connection()

    existing = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    if existing is None:
        connection.close()
        return None

    title = updates.get("title", existing["title"])
    description = updates.get(
        "description",
        existing["description"]
    )
    priority = updates.get(
        "priority",
        existing["priority"]
    )
    due_date = updates.get(
        "due_date",
        existing["due_date"]
    )

    connection.execute(
        """
        UPDATE tasks
        SET title = ?,
            description = ?,
            priority = ?,
            due_date = ?
        WHERE id = ?
        """,
        (
            title,
            description,
            priority,
            due_date,
            task_id,
        ),
    )

    connection.commit()

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    connection.close()

    return row_to_dict(row)


def complete_task(task_id):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE tasks
        SET completed = 1
        WHERE id = ?
        """,
        (task_id,),
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        return None

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    connection.close()

    return row_to_dict(row)


def delete_task(task_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,),
    )

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted


def search_tasks(query):
    connection = get_connection()

    search_text = f"%{query}%"

    rows = connection.execute(
        """
        SELECT * FROM tasks
        WHERE title LIKE ?
           OR description LIKE ?
        ORDER BY id
        """,
        (
            search_text,
            search_text,
        ),
    ).fetchall()

    connection.close()

    return [row_to_dict(row) for row in rows]