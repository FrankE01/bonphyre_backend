from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from models import CreateContributionInput, CreateContributionOUtput
from schemas import Contribution, Project, User
from utils import Session, authenticate_user_token, get_session, oauth2_scheme

router = APIRouter()


@router.post("/{project_id}/contribute", response_model=CreateContributionOUtput)
async def contribute(
    project_id: UUID,
    input: CreateContributionInput,
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):

    user: User = authenticate_user_token(token, session)

    project = session.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.deadline < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Project deadline has passed")

    contribution: Contribution = Contribution(
        user_id=user.id, project_id=project_id, amount=input.amount
    )

    session.add(contribution)
    session.commit()

    return contribution
