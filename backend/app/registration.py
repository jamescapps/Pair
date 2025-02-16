from fastapi import APIRouter

from ..schema.registration import RegistrationSchema
from ..services.registration import RegisterationService

router = APIRouter("v1/register", tags=["Registration"])


@router.post("/")
def register(registration_data: RegistrationSchema, svc: RegisterationService):
    return svc.sign_up(registration_data)
