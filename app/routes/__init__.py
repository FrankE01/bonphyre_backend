# isort:skip_file

from fastapi import APIRouter
from routes import user, project, contribution

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["user"])
router.include_router(contribution.router, prefix="/projects", tags=["projects"])
router.include_router(project.router, prefix="/projects", tags=["projects"])
