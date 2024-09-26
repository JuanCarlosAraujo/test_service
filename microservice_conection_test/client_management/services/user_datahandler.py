from datetime import datetime
from client_management.models import User
from client_management.schema import UserFormData

def build_user_from_form_data(form_data: UserFormData) -> User:
    
    json_data = form_data.json()
    json_data = json.loads(json_data)
    
    user = User(
        mail=form_data.mail,
        company_ID=form_data.company_ID,
        division_ID=form_data.division_ID,
        status_ID=form_data.status_ID,
        create_by=form_data.create_by,
        is_segura_user=form_data.is_segura_user,
    )
    
    return user

import json

def convert_form_to_json(form_data: UserFormData) -> str:
    print(form_data.json())
    return form_data.json()  