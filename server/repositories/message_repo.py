from sqlmodel import Session, select
from models.message_model import Message, MessageRole
from typing import List


def create_message(
    session: Session,
    case_id: int,
    content: str,
    role: MessageRole,
    citations: List[dict] = [],
):
    new_message = Message(
        case_id=case_id, content=content, role=role, citations=citations
    )
    session.add(new_message)
    session.commit()
    session.refresh(new_message)
    return new_message


def get_messages_by_caseId(session: Session, case_id: int):
    stmt = select(Message).where(Message.case_id == case_id).order_by(Message.id.asc())
    messages = session.exec(stmt).all()
    return messages
