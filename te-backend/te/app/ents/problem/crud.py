from typing import Any

from sqlalchemy.orm import Session

import app.core.security as security
from app.ents.base import crud_base
from app.ents.user import models, schema


def read_multi(db: Session, *, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create(db: Session, *, data: schema.UserCreate) -> models.User:
    data.password = security.get_password_hash(data.password)
    user = models.User(
        **(data.dict()),
        full_name=self.get_user_full_name(data),
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# def update(
#     db: Session,
#     *,
#     db_obj: models.User,
#     data: schema.UserUpdate | dict[str, Any],
# ) -> models.User:
#     if isinstance(data, dict):
#         update_data = data
#     else:
#         update_data = data.dict(exclude_unset=True)
#     if update_data["password"]:
#         hashed_password = security.get_password_hash(update_data["password"])
#         del update_data["password"]
#         update_data["hashed_password"] = hashed_password
#     return super().update(db, db_obj=db_obj, data=update_data)
