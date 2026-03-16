from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
from services import case_service, insight_service
from services import conversation_service
from schemas.case_schemas import (
    CaseRead,
    CaseUpdate,
    CaseCreate,
    AssetRead,
    RelationshipRead,
    EntityRead,
)
from schemas.chat_schemas import ChatInput

from sqlmodel import Session
from core.database import get_session
from core.s3 import s3

from typing import List
from dependencies import case_dependencies
from dependencies import auth_dependencies

router = APIRouter()


@router.post("/", status_code=201, response_model=CaseRead, summary="Create case")
def create_case(
    case_data: CaseCreate,
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
):
    """Create a new case for the current user."""
    return case_service.create_case(
        case_data=case_data, session=session, current_user=current_user
    )


@router.get("/", response_model=List[CaseRead], summary="Get cases for user")
def get_cases(
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
):
    """Retrieve all cases for the current user."""
    if current_user.role == "attorney":
        return case_service.get_cases_by_user_id(
            user_id=current_user.id, session=session
        )


@router.get("/{case_id}", response_model=CaseRead, summary="Get case by id")
def get_case_by_id(
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
    case=Depends(case_dependencies.verify_case_owner),
):
    """Retrieve a specific case by ID."""
    return case_service.get_case_by_Id(case_id=case.id, session=session)


@router.patch("/{case_id}", response_model=CaseRead, summary="Update case")
def update_case(
    case_data: CaseUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
    case=Depends(case_dependencies.verify_case_owner),
):
    """Update an existing case."""
    return case_service.update_case(
        case_id=case.id, case_data=case_data, session=session
    )


@router.get(
    "/{case_id}/assets", response_model=List[AssetRead], summary="Get case assets"
)
def get_case_assets(
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
    case=Depends(case_dependencies.verify_case_owner),
):
    """Retrieve all assets for a specific case."""
    assets = case_service.get_case_assets(case_id=case.id, session=session)
    return JSONResponse(
        content={
            "status": "success",
            "data": assets,
        }
    )


@router.post(
    "/{case_id}/assets/upload",
    response_model=AssetRead,
    status_code=201,
    summary="Upload case files",
)
async def upload_asset(
    file: UploadFile,
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
    case=Depends(case_dependencies.verify_case_owner),
):
    """Upload a new asset/file to a case."""
    return await case_service.upload_case_asset(
        case_id=case.id,
        file=file,
        session=session,
    )


@router.post(
    "/{case_id}/assets/{asset_id}/process",
    status_code=201,
    summary="Process case asset",
)
def process_asset(
    asset_id,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
    case=Depends(case_dependencies.verify_case_owner),
    asset=Depends(case_dependencies.verify_asset_owner),
):
    """Process an uploaded asset (extract text, generate embeddings, etc.)."""
    processed_asset = case_service.process_case_asset(
        case_id=case.id,
        asset_id=asset_id,
        file=asset,
        session=session,
        background_tasks=background_tasks,
    )

    return JSONResponse(content={"status": "success"})


@router.get("/{case_id}/conversation", summary="Get case conversation")
def get_case_conversation(
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
    case=Depends(case_dependencies.verify_case_owner),
):
    """Retrieve the conversation history for a case."""
    conversation = conversation_service.get_case_conversation(
        case_id=case.id, session=session
    )
    return JSONResponse(
        content={
            "status": "success",
            "data": [message.model_dump(mode="json") for message in conversation],
        }
    )


@router.post("/{case_id}/chat", summary="Chat with case data")
def chat(
    message: ChatInput,
    session: Session = Depends(get_session),
    dependencies=[Depends(auth_dependencies.get_current_user)],
    case=Depends(case_dependencies.verify_case_owner),
):
    """Send a message to chat with case data and get AI-powered response."""
    reply = conversation_service.reply(session, case.id, message.message)
    return JSONResponse(content={"reply": reply.model_dump(mode="json")})


@router.get("/{case_id}/extract-relationships", summary="Get case graph")
def extract_relationships(
    session: Session = Depends(get_session),
    dependencies=[Depends(auth_dependencies.get_current_user)],
    case=Depends(case_dependencies.verify_case_owner),
):
    """Generate or retrieve a summary of the case."""
    insight_service.get_entity_relationship(case_id=case.id, session=session)
    return JSONResponse(content={"status": "success"})


@router.get(
    "/{case_id}/relationships",
    response_model=List[RelationshipRead],
    summary="Get case graph",
)
def get_relationships(
    session: Session = Depends(get_session),
    dependencies=[Depends(auth_dependencies.get_current_user)],
    case=Depends(case_dependencies.verify_case_owner),
):
    """Generate or retrieve a summary of the case."""
    return insight_service.get_case_relationships(case_id=case.id, session=session)


@router.get(
    "/{case_id}/entities",
    response_model=List[EntityRead],
    summary="Get case graph",
)
def get_entities(
    session: Session = Depends(get_session),
    dependencies=[Depends(auth_dependencies.get_current_user)],
    case=Depends(case_dependencies.verify_asset_owner),
):
    """Generate or retrieve a summary of the case."""
    return insight_service.get_case_entities(case_id=case.id, session=session)
