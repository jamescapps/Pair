from fastapi import APIRouter
from services.auth import AuthService

router = APIRouter("/v1/auth", tags=["auth"])


@router.post("/login")
def login(svc: AuthService):
    return svc.login()


@router.post("/logout")
def logout(svc: AuthService):
    svc.logout()


@router.put("email/confirm")
def confirm_email_update(svc: AuthService):
    svc.confirm_emai_update()
