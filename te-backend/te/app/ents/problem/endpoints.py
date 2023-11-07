from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

import app.ents.problem.crud as problem_crud
import app.ents.problem.schema as problem_schema
import app.ents.user.crud as user_crud

router = APIRouter(prefix="/problems")


# @router.get(".list", response_model=list[problem_schema.ProproblemRead])
# def get_problems(
#     db: Session = Depends(dependencies.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     # _: str = Depends(dependencies.get_current_user),
# ) -> Any:
#     """
#     Retrieve Problems.
#     """
#     problems = crud.problem.read_multi(db, skip=skip, limit=limit)
#     return problems


# @router.post(".create", response_model=problem_schema.ProproblemRead)
# def create_problem(
#     *,
#     db: Session = Depends(dependencies.get_db),
#     data: problem_schema.ProproblemCreate,
#     # _=Depends(get_current_user),
# ) -> Any:
#     """
#     Create an Proproblem.
#     """
#     problem = user_crud.read_user_by_email(db, email=data.email)
#     if problem:
#         raise HTTPException(
#             status_code=400,
#             detail={
#                 "error": {
#                     "email": problem.name,
#                     "message": "The problem with this name already exists!",
#                 }
#             },
#         )

#     problem = crud.problem.create(db, data=data)
#     return problem


# @router.put(".info/{problem_id}", response_model=problem_schema.ProproblemRead)
# def update_problem(
#     *,
#     db: Session = Depends(dependencies.get_db),
#     data: problem_schema.ProproblemUpdate,
#     user: models.Proproblem = Depends(dependencies.get_current_user),
# ) -> Any:
#     """
#     Update Proproblem.
#     """
#     problem = problem.crud.read_user_by_id(db, id=problem.id)
#     if not problem:
#         raise HTTPException(
#             status_code=404,
#             detail={
#                 "error": {
#                     "email": problem.email,
#                     "message": "The problem with this name does not exist in the system",
#                 }
#             },
#         )
#     problem = problem_crud.update(db, db_obj=problem, data=data)
#     return user
