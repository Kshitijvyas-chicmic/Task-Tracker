from sqlalchemy.orm import Session
from models.user import User
from models.task import Task
from models.comment import Comment
from models.activity_log import ActivityLog
from models.role import Role
from models.permission import Permission

from langchain_core.documents import Document

def get_all_documents(db: Session):
    docs=[]

    # Tasks
    tasks=db.query(Task).all()
    content=f"There are total {len(tasks)} number of tasks. The list of the tasks is:\n"
    docs.append(Document(page_content=content,metadata={"table":"tasks","total_tasks":len(tasks)}))
    for t in tasks:
        content = f"Task #{t.task_id}: Title={t.title}, Description={t.description}, Status={t.status}, Priority={t.priority}, Assigned to= {t.assigned_to if t.assigned_to else 'None'}, Created by= {t.created_by if t.created_by else 'None'}"
        docs.append(Document(page_content=content, metadata={"table":"tasks", "task_id": t.task_id}))

     # Users
    users = db.query(User).all()
    content=f"There are total {len(users)} number of users. The list of the users is:\n"
    docs.append(Document(page_content=content,metadata={"table":"users","total_users":len(users)}))
    for u in users:
        content = f"User #{u.e_id}: Name={u.name}, Email={u.email}, Team={u.team}, Role={u.role.name if u.role else 'None'}"
        docs.append(Document(page_content=content, metadata={"table": "users","user_id":u.e_id}))

    # Comments
    comments = db.query(Comment).all()
    content=f"There are total {len(comments)} number of comments. The list of the comments is:\n"
    docs.append(Document(page_content=content,metadata={"table":"comments","total_comments":len(comments)}))
    for c in comments:
        content = f"Comment #{c.c_id} on Task #{c.task_id} by {c.user.name if c.user else 'Unknown'}: {c.content}"
        docs.append(Document(page_content=content, metadata={"table": "comments", "comment_id":c.c_id}))

    # Activity Logs
    logs = db.query(ActivityLog).all()
    content=f"There are total {len(logs)} number of activity logs. The list of the activity logs is:\n"
    docs.append(Document(page_content=content,metadata={"table":"activity_logs","total_logs":len(logs)}))
    for l in logs:
        content = f"ActivityLog #{l.id}: Actor={l.actor_id}, Action={l.action}, Entity={l.entity}#{l.entity_id}, Old={l.old_value}, New={l.new_value}, Timestamp={l.timestamp}"
        docs.append(Document(page_content=content, metadata={"table": "activity_logs", "log_id":l.id}))

    # Roles
    roles=db.query(Role).all()
    content=f"There are total {len(roles)} number of roles. The list of the roles is:\n"
    docs.append(Document(page_content=content,metadata={"table":"roles","total_roles":len(roles)}))
    for r in roles:
        content=f"Role #{r.r_id}, Name={r.name}"
        docs.append(Document(page_content=content, metadata={"table":"roles", "role_id":r.r_id}))

    return docs