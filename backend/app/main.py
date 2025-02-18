from fastapi import FastAPI

from .auth import router as auth_router
from .message import router as message_router
from .registration import router as registration_router
from .user import router as user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(message_router)
app.include_router(registration_router)
app.include_router(user_router)
