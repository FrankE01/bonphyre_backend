from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from models import CreateUserInput, CreateUserOutput, User, LoginUserInput
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from utils import get_password_hash, get_session, verify_password, create_access_token, verify_access_token
import os

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")


@router.post("/register")
async def register_user(
    input: CreateUserInput, session: Session = Depends(get_session)
):
    try:
        input.password = get_password_hash(input.password)

        user = User(**input.model_dump())

        session.add(user)
        session.commit()

        access_token = create_access_token(
            data={"sub": user.username} 
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email or username already exists.")
    
@router.post("/token", include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.query(User).filter(or_(User.username == form_data.username, User.email == form_data.username)).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password",
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password",
        )   
    

    access_token = create_access_token(
        data={"sub": user.username} 
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
async def login(form_data: LoginUserInput, session: Session = Depends(get_session)):
    user = session.query(User).filter(or_(User.username == form_data.username, User.email == form_data.username)).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password",
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password",
        )   
    

    access_token = create_access_token(
        data={"sub": user.username} 
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=CreateUserOutput)
async def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):

    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    username = payload.get("sub")

    user = session.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password",
        )
    return user
