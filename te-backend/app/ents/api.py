from app.ents.application.endpoints import (
    app_router,
    user_app_router,
    user_files_router,
)
from app.ents.company.endpoints import company_router, referral_router
from app.ents.home.endpoints import home_router
from app.ents.learning.endpoints import router as learning_router
from app.ents.problem.endpoints import router as problem_router
from app.ents.user.auth import router as login_router
from app.ents.user.endpoints import router as user_router
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(home_router, tags=["Home Endpoints"])

api_router.include_router(user_router, tags=["User Endpoints"])
api_router.include_router(login_router, tags=["User Login"])

api_router.include_router(app_router, tags=["Application Endpoints"])
api_router.include_router(user_files_router, tags=["User Files Endpoints"])
api_router.include_router(user_app_router, tags=["User Application Endpoints"])

api_router.include_router(company_router, tags=["Company Endpoints"])
api_router.include_router(referral_router, tags=["Referral Endpoints"])

api_router.include_router(learning_router, tags=["Learning Endpoints"])
api_router.include_router(problem_router, tags=["Problem Endpoints"])
