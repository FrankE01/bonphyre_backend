from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from models import CreateProjectInput, CreateProjectOutput, GetProjectOutput
from schemas import Project, User
from utils import Session, authenticate_user_token, get_session, oauth2_scheme

router = APIRouter()


@router.post("/", response_model=CreateProjectOutput)
async def create_project(
    input: CreateProjectInput,
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):

    user: User = authenticate_user_token(token, session)

    try:
        project = Project(**input.model_dump())

        session.add(project)
        session.commit()

        return project

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid input. Make sure the title and description are unique",
        )


@router.get("/", response_model=list[CreateProjectOutput])
async def get_projects(session: Session = Depends(get_session)):
    projects = session.query(Project).all()
    return projects


@router.get("/{project_id}", response_model=GetProjectOutput)
async def get_project(project_id: UUID, session: Session = Depends(get_session)):
    project: Project = session.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # contributors: list[str] = [user.username for user in project.contributors]
    # output = GetProjectOutput(**project.model_dump(), contributors=contributors, total_contributions=project.total_contributions)

    return project
