from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm

from app.algorithms import choose_next_task
from app.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.database import create_table
from app.models import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.repository import (
    complete_task,
    create_task,
    delete_task,
    get_all_tasks,
    get_task,
    search_tasks,
    update_task,
)
from app.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from app.weather import get_weather


#create_table()


app = FastAPI(
    title="Study Task Manager API",
    description="A beginner-friendly API for managing study tasks.",
    version="1.0.0",
)


# -------------------------
# HEALTH
# -------------------------


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


# -------------------------
# SIGNUP
# -------------------------


@app.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(user: UserCreate):

    existing_username = get_user_by_username(
        user.username
    )

    if existing_username is not None:
        raise HTTPException(
            status_code=400,
            detail="Username already exists.",
        )

    existing_email = get_user_by_email(
        user.email
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already exists.",
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = create_user(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
    )

    return new_user


# -------------------------
# LOGIN
# -------------------------


@app.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):

    user = get_user_by_username(
        form_data.username
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password.",
        )

    password_correct = verify_password(
        form_data.password,
        user["password_hash"],
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password.",
        )

    access_token = create_access_token(
        user["username"]
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# -------------------------
# CURRENT USER
# -------------------------


@app.get(
    "/me",
    response_model=UserResponse,
)
def read_current_user(
    current_user=Depends(get_current_user),
):
    return current_user


# -------------------------
# TASKS
# -------------------------


@app.get(
    "/tasks",
    response_model=list[TaskResponse],
)
def read_all_tasks():
    return get_all_tasks()


@app.get(
    "/tasks/search",
    response_model=list[TaskResponse],
)
def search_for_tasks(query: str):
    return search_tasks(query)


@app.get(
    "/tasks/next",
    response_model=TaskResponse,
)
def read_next_task():

    tasks = get_all_tasks()

    task = choose_next_task(tasks)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="No incomplete tasks found.",
        )

    return task


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
def read_task(task_id: int):

    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return task


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_task(task: TaskCreate):

    due_date = None

    if task.due_date is not None:
        due_date = task.due_date.isoformat()

    return create_task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=due_date,
    )


@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
def edit_task(
    task_id: int,
    task: TaskUpdate,
):

    updates = task.model_dump(
        exclude_unset=True
    )

    if (
        "due_date" in updates
        and updates["due_date"] is not None
    ):
        updates["due_date"] = (
            updates["due_date"].isoformat()
        )

    updated_task = update_task(
        task_id,
        updates,
    )

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return updated_task


@app.patch(
    "/tasks/{task_id}/complete",
    response_model=TaskResponse,
)
def mark_task_complete(task_id: int):

    task = complete_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_task(task_id: int):

    deleted = delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found.",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


# -------------------------
# WEATHER
# -------------------------


@app.get("/weather")
def weather(
    latitude: float,
    longitude: float,
):

    try:
        return get_weather(
            latitude=latitude,
            longitude=longitude,
        )

    except RuntimeError:
        raise HTTPException(
            status_code=502,
            detail="Weather service is unavailable.",
        )
@app.get("/")
def home():
    return {
        "message": "Study Task Manager API is running",
        "docs": "/docs"
    }