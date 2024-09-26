from sqlalchemy.orm import Session
from client_management.models import User, UserModel, UserResponse
from datetime import datetime
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError


def search_users_service(
    user_ID: Optional[int],
    mail: Optional[str],
    company_ID: Optional[int],
    division_ID: Optional[int],
    status_ID: Optional[int],
    is_segura_user: Optional[bool],
    db: Session
) -> UserResponse:
    try:
        query = db.query(UserModel)

        if user_ID is not None:
            query = query.filter(UserModel.user_ID == user_ID)
        if mail is not None:
            query = query.filter(UserModel.mail == mail)
        if company_ID is not None:
            query = query.filter(UserModel.company_ID == company_ID)
        if division_ID is not None:
            query = query.filter(UserModel.division_ID == division_ID)
        if status_ID is not None:
            query = query.filter(UserModel.status_ID == status_ID)
        if is_segura_user is not None:
            query = query.filter(UserModel.is_segura_user == is_segura_user)

        users = query.all()

        if not users:
            return UserResponse(status="error", message="No users found", data=None)

        return UserResponse(
            status="success",
            message="Users retrieved successfully.",
            data=[User.from_orm(user) for user in users]
        )
    
    except Exception as e:
        return UserResponse(status="error", message=f"Unable to perform the search. Error: {str(e)}", data=None)

def create_user_service(user: User, db: Session) -> UserResponse:
    try:
        db_user = UserModel(
            mail=user.mail,
            company_ID=user.company_ID,
            division_ID=user.division_ID,
            status_ID=user.status_ID,
            fechadecreacion=datetime.utcnow(),
            create_by=user.create_by,
            is_segura_user=user.is_segura_user
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return get_user_by_id_service(db_user.user_ID, db)

    except SQLAlchemyError as e:
        return UserResponse(status="error", message=str(e), data=None)
    except Exception as e:
        return UserResponse(status="error", message="An unexpected error occurred: " + str(e), data=None)

def get_users_service(db: Session):
    users = db.query(UserModel).all()
    return [UserResponse(status="success", message="", data=User.from_orm(user)) for user in users]


def get_user_by_id_service(user_id: int, db: Session) -> UserResponse:
    try:
        user = db.query(UserModel).filter(UserModel.user_ID == user_id).first()
        if not user:
            return UserResponse(status="error", message="User not found", data=None)
        
        user_data = User.from_orm(user)
        return UserResponse(status="success", message="", data=user_data)
        
    except SQLAlchemyError as e:
        return UserResponse(status="error", message=str(e), data=None)
    
def update_user_service(user_id: int, user: User, db: Session) -> UserResponse:
    db_user = db.query(UserModel).filter(UserModel.user_ID == user_id).first()
    if not db_user:
        return UserResponse(status="error", message="User not found", data=None)

    db_user.mail = user.mail
    db_user.company_ID = user.company_ID
    db_user.division_ID = user.division_ID
    db_user.status_ID = user.status_ID
    db_user.is_segura_user = user.is_segura_user
    db.commit()
    
    return UserResponse(status="success", message="User updated successfully.", data=user)

def delete_user_service(user_id: int, db: Session) -> UserResponse:
    db_user = db.query(UserModel).filter(UserModel.user_ID == user_id).first()
    if not db_user:
        return UserResponse(status="error", message="User not found", data=None)

    db.delete(db_user)
    db.commit()
    
    return UserResponse(status="success", message="User deleted successfully.", data=None)
