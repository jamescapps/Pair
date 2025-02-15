from fastapi import APIRouter

from services.message import MessageService

router = APIRouter(prefix="/v1/message", tags=["message"])


# TODO token authentication, svc dependency, response model


@router.get("/number/unread")
def get_num_of_unread_messages(user_id: int, svc: MessageService):
    return svc.get_num_of_unread_messages(user_id)


@router.get("/")
def get_messages(user_id: int, svc: MessageService):
    return svc.get_messages


# TODO send to username instead of ID maybe
@router.post("/send")
def send_message(from_user_id: int, to_user_id: int, svc: MessageService):
    svc.send_message(from_user_id, to_user_id)
