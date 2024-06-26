from typing import Any

import app.database.session as session
import app.ents.application.crud as application_crud
import app.ents.application.schema as application_schema
import app.ents.learning.crud as learning_crud
import app.ents.learning.schema as learning_schema
import app.ents.user.dependencies as user_dependencies
import app.ents.user.models as user_models
from app.core.settings import settings
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

router = APIRouter(prefix="/learning")


@router.get(
    ".lessons.list",
    response_model=dict[str, list[learning_schema.LessonRead]],
)
def get_lessons(
    db: Session = Depends(session.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve Problems.
    """
    lessons = learning_crud.read_lessons(db, skip=skip, limit=limit)
    return {
        "lessons": [learning_schema.LessonRead(**vars(lesson)) for lesson in lessons]
    }


@router.post(
    ".lessons.create",
    response_model=dict[str, learning_schema.LessonRead],
)
def add_lesson(
    db: Session = Depends(session.get_db),
    *,
    data: learning_schema.LessonCreate,
    current_user: user_models.User = Depends(
        user_dependencies.get_current_user_contributor
    ),
) -> Any:
    """
    Create a  lesson.
    """
    data.uploader = current_user.id
    lesson = learning_crud.create_lesson(db, data=data)

    return {"lesson": learning_schema.LessonRead(**vars(lesson))}


@router.post(
    ".file.upload",
    response_model=dict[str, application_schema.FileUpload],
)
def lesson_file_upload(
    *,
    db: Session = Depends(session.get_db),
    file: UploadFile,
    current_user: user_models.User = Depends(user_dependencies.get_current_user),
) -> Any:
    """
    Create other lesson.
    """
    uploaded_file = application_crud.upload_file(
        file=file, parent=settings.GDRIVE_LESSONS
    )
    return {"file": uploaded_file}
