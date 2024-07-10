from sqlalchemy.orm import Session
from . import models


# CRUD: Create, Read, Update, Delete <-- operations

# event that reads from fastAPI and creates a new translation in the database
# function: triggered by a FastAPI endpoint to create a new task
def create_translation_task(db: Session, text: str, Languages: list):
    # method 1
    task = models.TranslationTask(text=text, languages=Languages)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# used by FastAPI endpoint to get task details
# Function: retrieves translation tasks from the database
def get_translation_task(db: Session, task_id: int):
    return db.query(models.TranslationTask).filter(models.TranslationTask.id == task_id).first()

# method 2, different event --> update the status of translation task to "completed"
# Function: triggered by a FastAPI endpoint to update an existing task
def update_translation_task(db: Session, task_id: int, translation: dict):
    task = db.query(models.TranslationTask).filter(models.TranslationTask.id == task_id).first()
    task.status = "completed"
    db.commit()

    # refresh to reflect latest database state
    db.refresh(task)

    # return updated task
    return task
