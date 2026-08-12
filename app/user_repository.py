from datetime import datetime

from app.database import get_connection


def row_to_user_dict(row):
    if row is None:
        return None

    return {
        "id": row["id"],
        "username": row["username"],
        "email": row["email"],
        "password_hash": row["password_hash"],
        "created_at": row["created_at"],
    }


def create_user(username, email, password_hash):
    connection = get_connection()

    created_at = datetime.now().isoformat()

    cursor = connection.execute(
        """
        INSERT INTO users
        (username, email, password_hash, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            email,
            password_hash,
            created_at,
        ),
    )

    connection.commit()

    user_id = cursor.lastrowid

    row = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()

    connection.close()

    return row_to_user_dict(row)


def get_user_by_username(username):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,),
    ).fetchone()

    connection.close()

    return row_to_user_dict(row)


def get_user_by_email(email):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,),
    ).fetchone()

    connection.close()

    return row_to_user_dict(row)