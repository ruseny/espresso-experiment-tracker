from dotenv import load_dotenv
import os
from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi import Depends

load_dotenv()


driver = os.getenv("DB_DRIVER")
connector = os.getenv("DB_CONNECTOR")
user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

db_path = f"{driver}+{connector}://{user}:{password}@{host}:{port}/{db_name}"
db_engine = create_engine(db_path, echo=True)
def get_session():
    with Session(db_engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]