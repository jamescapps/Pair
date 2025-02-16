from sqlalchemy.orm import Session


class MessageService(object):
    def __init__(self, session: Session):
        self.sesssion = session

    def get_num_of_unread_messages(self, user_id: int):
        pass

    def get_messages(self, user_id: int):
        pass

    def send_message(self, from_user_id: int, to_user_id: int):
        pass

    def mark_message_as_seen(self, user_id: int, message_id: int):
        pass

    def delete_message_(self, user_id: int, message_id: int):
        pass

    def reply(self, user_id: int, message_id: int):
        pass
