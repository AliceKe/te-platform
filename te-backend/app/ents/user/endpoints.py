from typing import Any
import logging
import app.database.session as session
import app.ents.user.auth as user_auth
import app.ents.user.crud as user_crud
import app.ents.user.dependencies as user_dependencies
import app.ents.user.models as user_models
import app.ents.user.schema as user_schema
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users")


@router.post(".login")
def login_user(token=Depends(user_auth.login_access_token)) -> Any:
    """
    Log User in.
    """
    return {"token": token}


# @router.get(
#     ".mentee.list", response_model=dict[str, list[user_schema.UserRead]]
# )
# def get_mentees(
#     db: Session = Depends(session.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     _: user_models.User = Depends(user_dependencies.get_current_mentor),
# ) -> Any:
#     """
#     Retrieve all active mentees.
#     """
#     mentees = user_crud.read_users_by_role(
#         db, skip=skip, limit=limit, role=user_schema.UserRoles.mentee
#     )
#     return {
#         "mentees": [user_schema.UserRead(**vars(mentee)) for mentee in mentees]
#     }


# @router.get(
#     ".mentor.list", response_model=dict[str, list[user_schema.UserRead]]
# )
# def get_mentors(
#     db: Session = Depends(session.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     _: user_models.User = Depends(user_dependencies.get_current_mentor),
# ) -> Any:
#     """
#     Retrieve all active mentors.
#     """
#     mentors = user_crud.read_users_by_role(
#         db, skip=skip, limit=limit, role=user_schema.UserRoles.mentor
#     )
#     return {
#         "mentors": [user_schema.UserRead(**vars(mentor)) for mentor in mentors]
#     }


# @router.get(
#     ".contributor.list", response_model=dict[str, list[user_schema.UserRead]]
# )
# def get_contributors(
#     db: Session = Depends(session.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     _: user_models.User = Depends(
#         user_dependencies.get_current_user_contributor
#     ),
# ) -> Any:
#     """
#     Retrieve all active contributors.
#     """
#     contributors = user_crud.read_users_by_role(
#         db, skip=skip, limit=limit, role=user_schema.UserRoles.contributor
#     )
#     return {
#         "contributors": [
#             user_schema.UserRead(**vars(contributor))
#             for contributor in contributors
#         ]
#     }


# @router.get(".team.list", response_model=dict[str, list[user_schema.UserRead]])
# def get_team(
#     db: Session = Depends(session.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     _: user_models.User = Depends(user_dependencies.get_current_user_team),
# ) -> Any:
#     """
#     Retrieve all active team.
#     """
#     team = user_crud.read_users_by_role(
#         db, skip=skip, limit=limit, role=user_schema.UserRoles.team
#     )
#     return {"team": [user_schema.UserRead(**vars(member)) for member in team]}


# @router.get(".admin.list", response_model=dict[str, list[user_schema.UserRead]])
# def get_admins(
#     db: Session = Depends(session.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     _: user_models.User = Depends(user_dependencies.get_current_user_admin),
# ) -> Any:
#     """
#     Retrieve all active admins.
#     """
#     admins = user_crud.read_users_by_role(
#         db, skip=skip, limit=limit, role=user_schema.UserRoles.admin
#     )
#     return {
#         "admins": [user_schema.UserRead(**vars(member)) for member in admins]
#     }


@router.get(".role.list", response_model=dict[str, list[user_schema.UserRead]])
def get_users_by_role(
    db: Session = Depends(session.get_db),
    *,
    skip: int = 0,
    limit: int = 100,
    role: user_schema.UserRoles = user_schema.UserRoles.mentee,
    _: user_models.User = Depends(user_dependencies.get_current_user_by_role),
) -> Any:
    """
    Retrieve all active admins.
    """
    users = user_crud.read_users_by_role(db, role=role, skip=skip, limit=limit)
    return {"users": [user_schema.UserRead(**vars(user)) for user in users]}


@router.get(".{user_id}.info", response_model=dict[str, user_schema.UserRead])
def get_user_by_id(
    db: Session = Depends(session.get_db),
    *,
    user_id: int,
    _: user_models.User = Depends(user_dependencies.get_current_user_by_role),
) -> Any:
    """
    Retrieve all active admins.
    """
    logging.info("Getting user info")
    user = user_crud.read_user_by_id(db, id=user_id)
    return {"user": user_schema.UserRead(**vars(user))}


# @router.get(".list", response_model=dict[str, list[user_schema.UserRead]])
# def get_all_users(
#     db: Session = Depends(session.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: user_models.User = Depends(
#         user_dependencies.get_current_user_team
#     ),
# ) -> Any:
#     """
#     Retrieve all active users.
#     """
#     users = user_crud.read_users_by_base_role(
#         db, skip=skip, limit=limit, role=user_schema.UserRoles.guest
#     )
#     return {"users": [user_schema.UserRead(**vars(user)) for user in users]}


@router.post(".create", response_model=dict[str, user_schema.UserRead])
def create_user(
    *,
    db: Session = Depends(session.get_db),
    data: user_schema.UserCreate,
) -> Any:
    """
    Create an User.
    """
    new_user = user_crud.create_user(db, data=data)
    return {"user": user_schema.UserRead(**vars(new_user))}


@router.get(".{user_id}.essay", response_model=user_schema.Essay)
def get_essay(
    db: Session = Depends(session.get_db),
    *,
    user_id: int,
    _: user_models.User = Depends(user_dependencies.get_current_user),
):
    essay = user_crud.read_user_essay(db, user_id=user_id)
    return user_schema.Essay(essay=essay)


@router.post(".{user_id}.essay", response_model=user_schema.Essay)
def update_essay(
    db: Session = Depends(session.get_db),
    *,
    user_id: int,
    data: user_schema.Essay,
    _: user_models.User = Depends(user_dependencies.get_current_user),
):
    essay = user_crud.add_user_essay(db, user_id=user_id, data=data)
    return user_schema.Essay(essay=essay)
