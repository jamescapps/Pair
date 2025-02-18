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
    svc.session.commit()


@router.put("/account")
def edit_user(user_id: int, profile_data: ProfileSchema, svc: UserService):
    svc.edit_user(user_id, profile_data)
    svc.session.commt()


@router.delete("/account")
def delete_user(user_id: int, svc: UserService):
    svc.delete_user(user_id)
    svc.session.commit()


@router.put("/account/deactivate")
def deactivate_account(user_id: int, svc: UserService):
    svc.deactivate_account(user_id)
    svc.session.commit()


@router.get("/usernames")
def suggest_usernames(user_id: int, svc: UserService):
    return svc.suggest_usernames(user_id)


@router.post("/first-name/show")
def show_first_name(user_id: int, permission_granted_for_id: int, svc: UserService):
    svc.show_first_name(user_id, permission_granted_for_id)
    svc.session.commit()


@router.delete("/first-name/un-show")
def un_show_first_name(user_id: int, permission_granted_for_id: int, svc: UserService):
    svc.un_show_first_nameshow_first_name(user_id, permission_granted_for_id)
    svc.session.commit()
