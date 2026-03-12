from agents.chat_agent.agent import ChatAgent
from sqlmodel import Session
from repositories import message_repo

agent = ChatAgent()


def reply(session: Session, case_id: int, message: str):
    message_repo.create_message(session, case_id, message, "user")
    response = agent.reply(message, case_id)
    message_repo.create_message(
        session=session,
        case_id=case_id,
        content=response.response,
        citations=response.citations,
        role="assistant",
    )
    return response


def get_case_conversation(session: Session, case_id: int):
    return message_repo.get_messages_by_case_id(session=session, case_id=case_id)
