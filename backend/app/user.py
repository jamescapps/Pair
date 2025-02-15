from fastapi import APIRouter
from services.user import UserService
from schema.profile import ProfileSchema

router = APIRouter(prefix="/v1/user", tags=["user"])

# TODO token authentication, svc dependency, response model

@router.get("/account")
def get_user(user_id: int, svc: UserService):
    return svc.get_user(user_id)

@router.post("/account")
def add_user(profile_data: ProfileSchema, svc: UserService):
    svc.create_user(profile_data)

@router.put("/account")
def edit_user(user_id: int, profile_data: ProfileSchema, svc: UserService):
    return svc.edit_user(user_id, profile_data)

@router.delete("/account")
def delete_user(user_id: int, svc: UserService):
    svc.delete_user(user_id)

@router.put("/account/deactivate")
def deactivate_account(user_id: int, svc: UserService)
    svc.deactivate_account(user_id)
