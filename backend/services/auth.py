class AuthService(object):
    def __init__(self):
        ...

    def hash_password(self, password: str):
        ...

    def login(self):
        ...

    def logout(self):
        ...

    def generate_token(self):
        ...

    def send_email_update_verification(self, email: str):
        ...

    def confirm_emai_update(self):
        ...
