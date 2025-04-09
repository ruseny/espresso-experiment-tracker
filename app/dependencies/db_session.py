import json
from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi import Depends

with open("credentials/db_login.json", "r") as f:
    db_login = json.load(f)
db_path = f"mysql://{db_login['user']}:{db_login['password']}@{db_login['host']}/{db_login['db_name']}"
db_engine = create_engine(db_path)
def get_session():
    with Session(db_engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]