from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from models.case_model import Case, CaseStatus
from models.asset_model import Asset
from models.case_summary import CaseSummary
import json
from schemas.case_schemas import CaseUpdate


def create_case(session: Session, case_data: Case, current_user):
    new_case = Case(
        case_number=case_data.case_number,
        case_name=case_data.case_name,
        opposing_party=case_data.opposing_party,
        client=case_data.client,
        status=CaseStatus.active,
        user_id=current_user.id,
    )
    session.add(new_case)
    session.commit()
    session.refresh(new_case)
    return new_case


def update_case(session: Session, case_id: int, case_data: CaseUpdate):
    case = get_case_by_id(session, case_id)
    update_data = case_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(case, key, value)

    session.add(case)
    session.commit()
    session.refresh(case)
    return case


def get_case_by_id(session: Session, case_id: int):
    stmt = (
        select(Case)
        .where(Case.id == case_id)
        .options(
            selectinload(Case.assets),
        )
    )
    case = session.exec(stmt).first()
    return case


def get_cases_by_userId(session: Session, user_id: int):
    stmt = select(Case).filter(Case.user_id == user_id)
    cases = session.exec(stmt).all()
    return cases


def create_asset(session: Session, asset_data, case_id: int):
    new_asset = Asset(
        case_id=case_id,
        asset_name=asset_data["file_name"],
        asset_URL=asset_data["file_url"],
    )
    session.add(new_asset)
    session.commit()
    session.refresh(new_asset)
    return new_asset


def get_asset_by_id(session: Session, asset_id: int):
    stmt = select(Asset).filter(Asset.id == asset_id)
    asset = session.exec(stmt).first()
    return asset


def get_case_assets(session: Session, case_id: int):
    stmt = select(Asset).where(Asset.case_id == case_id).order_by(Asset.id.asc())
    assets = session.exec(stmt).all()
    return assets


def create_summary(session: Session, summary_data):

    content = summary_data["content"]
    if not isinstance(content, str):
        content = json.dumps(content)

    new_summary = CaseSummary(
        case_id=summary_data["case_id"],
        content=content,
        url=summary_data["url"],
    )
    session.add(new_summary)
    session.commit()
    session.refresh(new_summary)
    return new_summary


def get_case_summary(session: Session, case_id: int):
    stmt = select(CaseSummary).filter(CaseSummary.case_id == case_id)
    summary = session.exec(stmt).first()

    if summary and summary.content:
        try:
            summary.content = json.loads(summary.content)
        except (json.JSONDecodeError, TypeError):
            # If it's not valid JSON, keep it as is
            pass

    return summary
