
from pydantic import BaseSettings



class Settings(BaseSettings):
    secret: str
    db: str
    sender: str
    receiver: str
    password: str





    class Config:
        env_file = ".env"

settings = Settings()
    