from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from services import case_service
from services import conversation_service
from schemas.case_schemas import CaseRead, CaseUpdate, CaseCreate
from schemas.chat_schemas import ChatInput

from sqlmodel import Session
from core.database import get_session
from core.s3 import s3

from typing import List
from dependencies import case_dependencies
from dependencies import auth_dependencies

from agents.summarizer_agent.agent import SummarizerAgent

router = APIRouter()

# ============================================================================
# CASE CRUD OPERATIONS
# ============================================================================


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
        return case_service.get_cases_by_userId(
            user_id=current_user.id, session=session
        )


@router.get("/{case_id}", summary="Get case by id")
def get_case_by_id(
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
    case=Depends(case_dependencies.get_owned_case),
):
    """Retrieve a specific case by ID."""
    caseModel = case_service.get_case_by_Id(case_id=case.id, session=session)
    return JSONResponse(
        content={
            "status": "success",
            "data": {
                **caseModel.model_dump(mode="json"),
                "assets": [
                    {
                        "id": asset.id,
                        "name": asset.asset_name,
                        "url": asset.asset_URL,
                    }
                    for asset in caseModel.assets
                ],
            },
        }
    )


@router.patch("/{case_id}", response_model=CaseRead, summary="Update case")
def update_case(
    case_data: CaseUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
    case=Depends(case_dependencies.get_owned_case),
):
    """Update an existing case."""
    return case_service.update_case(
        case_id=case.id, case_data=case_data, session=session
    )


# ============================================================================
# CASE ASSETS OPERATIONS
# ============================================================================


@router.get("/{case_id}/assets", summary="Get case assets")
def get_case_assets(
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
    case=Depends(case_dependencies.get_owned_case),
):
    """Retrieve all assets for a specific case."""
    assets = case_service.get_case_assets(case_id=case.id, session=session)
    return JSONResponse(
        content={
            "status": "success",
            "data": [asset.model_dump(mode="json") for asset in assets],
        }
    )


@router.post("/{case_id}/assets/upload", status_code=201, summary="Upload case files")
async def upload_asset(
    file: UploadFile,
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
    case=Depends(case_dependencies.get_owned_case),
):
    """Upload a new asset/file to a case."""
    asset = await case_service.upload_case_asset(
        case_id=case.id,
        file=file,
        session=session,
    )

    return JSONResponse(
        content={"status": "success", "data": asset.model_dump(mode="json")}
    )


@router.post(
    "/{case_id}/assets/{asset_id}/process",
    status_code=201,
    summary="Process case asset",
)
async def process_asset(
    asset_id,
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
    case=Depends(case_dependencies.get_owned_case),
    asset=Depends(case_dependencies.get_asset_with_verification),
):
    """Process an uploaded asset (extract text, generate embeddings, etc.)."""
    processed_asset = await case_service.process_case_asset(
        case_id=case.id, asset_id=asset_id, file=asset, session=session
    )

    return JSONResponse(content={"status": "success"})


# ============================================================================
# CONVERSATION & CHAT OPERATIONS
# ============================================================================


@router.get("/{case_id}/conversation", summary="Get case conversation")
def get_case_conversation(
    session: Session = Depends(get_session),
    current_user=Depends(auth_dependencies.get_current_user),
    case=Depends(case_dependencies.get_owned_case),
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
    case=Depends(case_dependencies.get_owned_case),
):
    """Send a message to chat with case data and get AI-powered response."""
    reply = conversation_service.reply(session, case.id, message.message)
    return JSONResponse(content={"reply": reply.model_dump(mode="json")})


@router.get("/{case_id}/summary", summary="Get case summary")
def get_case_summary(
    session: Session = Depends(get_session),
    dependencies=[Depends(auth_dependencies.get_current_user)],
    case=Depends(case_dependencies.get_owned_case),
):
    """Generate or retrieve a summary of the case."""
    return case_service.get_case_summary(case.id, session)
