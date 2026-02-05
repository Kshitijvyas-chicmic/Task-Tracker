from langchain_core.tools import tool
from core.utils.database import SessionLocal
from core.utils.redis_client import redis_client
import json
from models.task import Task
from models.comment import Comment
from models.user import User


@tool
def list_tasks() -> str:
    """
    Provide list of all the tasks available
    """
    cache_key = "tasks:all"

    cached = redis_client.get(cache_key)
    if cached:
        tasks = json.loads(cached)
    else:
        db = SessionLocal()
        try:
            rows = db.query(Task).all()
            tasks = [
                {
                    "id": t.task_id,
                    "title": t.title,
                    "status": t.status,
                    "priority": t.priority
                }
                for t in rows
            ]
            redis_client.set(cache_key, json.dumps(tasks))
        finally:
            db.close()

    return "Here are your tasks:\n" + "\n".join(
        f"Task #{t['id']}: {t['title']} ({t['status']})"
        for t in tasks
    )

@tool
def create_task(title: str, description: str, status="pending", priority="medium") -> str:
    """
    Create a task with given values:
    arguments:
    title: name of the task,
    description: description of the task,
    other arguments like status, priority are optional and have default values.
    """
    
    db = SessionLocal()
    try:
        task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        cache_key = "tasks:all"
        cached = redis_client.get(cache_key)

        if cached:
            tasks = json.loads(cached)
            tasks.append({
                "id": task.task_id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority
            })
            redis_client.set(cache_key, json.dumps(tasks))

        return f"Task #{task.task_id} created successfully."
    finally:
        db.close()


@tool
def delete_task(task_id: int) -> str:
    """
    Delete the task with given id
    arguments:
    task_id: it's a integer value which identifies the task to be deleted.
    """

    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.task_id == task_id).first()
        if not task:
            return f"Task #{task_id} not found."

        db.delete(task)
        db.commit()

        cache_key = "tasks:all"
        cached = redis_client.get(cache_key)

        if cached:
            tasks = json.loads(cached)
            tasks = [t for t in tasks if t["id"] != task_id]
            redis_client.set(cache_key, json.dumps(tasks))

        return f"Task #{task_id} deleted."
    finally:
        db.close()

@tool
def add_comment(task_id: int, content: str) -> str:
    """Add a comment to an existing task."""

    db = SessionLocal()
    try:
        comment = Comment(task_id=task_id, content=content)
        db.add(comment)
        db.commit()
        db.refresh(comment)

        cache_key = f"task:{task_id}:comments"
        cached = redis_client.get(cache_key)

        if cached:
            comments = json.loads(cached)
            comments.append({
                "id": comment.id,
                "task_id": task_id,
                "content": comment.content
            })
            redis_client.set(cache_key, json.dumps(comments))

        return f"Comment added to task #{task_id}."
    finally:
        db.close()

@tool
def list_comments(task_id: int) -> str:
    """List comments for a specific task."""

    cache_key = f"task:{task_id}:comments"

    cached = redis_client.get(cache_key)
    if cached:
        comments = json.loads(cached)
    else:
        db = SessionLocal()
        try:
            rows = db.query(Comment).filter(Comment.task_id == task_id).all()
            comments = [
                {
                    "id": c.id,
                    "task_id": c.task_id,
                    "content": c.content
                }
                for c in rows
            ]
            redis_client.set(cache_key, json.dumps(comments))
        finally:
            db.close()

    if not comments:
        return f"No comments found for task #{task_id}."

    return f"Comments for task #{task_id}:\n" + "\n".join(
        f"- {c['content']}" for c in comments
    )

@tool
def list_users() -> str:
    """Fetch and return a formatted list of users."""

    cache_key = "users:all"

    cached = redis_client.get(cache_key)
    if cached:
        users = json.loads(cached)
    else:
        db = SessionLocal()
        try:
            rows = db.query(User).all()
            users = [
                {
                    "id": u.e_id,
                    "name": u.name,
                    "role": u.role.name
                }
                for u in rows
            ]
            redis_client.set(cache_key, json.dumps(users))
        finally:
            db.close()

    if not users:
        return "No users found."

    return "Here are the users:\n" + "\n".join(
        f"User #{u['id']}: {u['name']} (role={u['role']})"
        for u in users
    )