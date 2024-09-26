from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlalchemy.orm import Session
from client_management.models import User, UserResponse, UserModel
from typing import List
from client_management.services.user_crud_service import (  # Asegúrate de que estas funciones estén definidas en services.py
    create_user_service,
    get_users_service,
    get_user_by_id_service,
    update_user_service,
    delete_user_service,
    search_users_service
)
from client_management.services.user_datahandler import build_user_from_form_data
from config.db_connection import get_db
from client_management.schema import UserFormData

user = APIRouter()

@user.post("/users", response_model=UserResponse)
async def create_user(
    is_segura_user: bool = Form(False),
    mail: str = Form(...),
    company_ID: int = Form(...),
    division_ID: int = Form(...),
    status_ID: int = Form(...),
    create_by: int = Form(...),
    db: Session = Depends(get_db)
):
    form_data = UserFormData(
        is_segura_user=is_segura_user,
        mail=mail,
        company_ID=company_ID,
        division_ID=division_ID,
        status_ID=status_ID,
        create_by=create_by
    )


    user = build_user_from_form_data(form_data)

    return create_user_service(user, db)


@user.get("/search_users", response_model=UserResponse)
def search_users(
    user_ID: int = Query(None), 
    mail: str = Query(None),
    company_ID: int = Query(None),
    division_ID: int = Query(None),
    status_ID: int = Query(None),
    is_segura_user: str = Query(None),
    db: Session = Depends(get_db)
):

    response = search_users_service(
        user_ID=user_ID,
        mail=mail,
        company_ID=company_ID,
        division_ID=division_ID,
        status_ID=status_ID,
        is_segura_user=is_segura_user,
        db=db
    )
    return response


@user.get("/users", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return get_users_service(db)

@user.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id_service(user_id, db)

@user.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    return update_user_service(user_id, user, db)

@user.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user_service(user_id, db)