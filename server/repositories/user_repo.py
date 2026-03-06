from sqlmodel import Session, select
from schemas.user_schemas import CreateUser
from models.user_model import User, RoleEnum


def create_user(
    session: Session,
    username: str,
    hashed_password: str,
    role: str = RoleEnum.ATTORNEY,
    created_by: int = None,
):
    user = User(
        username=username, password=hashed_password, role=role, created_by=created_by
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(session: Session, username: str):
    stmt = select(User).filter(User.username == username)
    user = session.exec(stmt).first()
    if user:
        return user
