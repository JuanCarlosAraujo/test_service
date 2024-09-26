from pydantic import BaseModel

class UserFormData(BaseModel):
    is_segura_user: bool
    mail: str
    company_ID: int
    division_ID: int
    status_ID: int
    create_by: int