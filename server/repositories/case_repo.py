from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from models.case_model import Case, CaseStatus
from models.asset_model import Asset, AssetStatus
from models.case_summary import CaseSummary
from schemas.case_schemas import CaseCreate, CaseUpdate, AssetUpdate
from core.exceptions import NotFoundException


# ── Case ──────────────────────────────────────────────────────────────────────


def create_case(session: Session, case_data: CaseCreate, user_id: int) -> Case:
    new_case = Case(
        **case_data.model_dump(),
        status=CaseStatus.active,
        user_id=user_id,
    )
    session.add(new_case)
    session.commit()
    session.refresh(new_case)
    return new_case


def update_case(session: Session, case_id: int, case_data: CaseUpdate) -> Case:
    case = get_case_by_id(session, case_id)
    update_data = case_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(case, key, value)

    session.add(case)
    session.commit()
    session.refresh(case)
    return case


def get_case_by_id(session: Session, case_id: int) -> Case:
    stmt = (
        select(Case)
        .where(Case.id == case_id)
        .options(
            selectinload(Case.assets),
        )
    )
    case = session.exec(stmt).first()
    if not case:
        raise NotFoundException(f"Case {case_id} not found")
    return case


def get_cases_by_user_id(session: Session, user_id: int) -> list[Case]:
    stmt = select(Case).where(Case.user_id == user_id)
    return session.exec(stmt).all()


def create_asset(session: Session, asset_data: dict, case_id: int) -> Asset:
    new_asset = Asset(
        case_id=case_id,
        asset_name=asset_data["file_name"],
        asset_URL=asset_data["file_url"],
    )
    session.add(new_asset)
    session.commit()
    session.refresh(new_asset)
    return new_asset


def get_asset_by_id(session: Session, asset_id: int) -> Asset:
    stmt = select(Asset).where(Asset.id == asset_id)
    asset = session.exec(stmt).first()
    if not asset:
        raise NotFoundException(f"Asset {asset_id} not found")
    return asset


def update_asset(session: Session, asset_id: int, asset_data: AssetUpdate) -> Case:
    asset = get_asset_by_id(session, asset_id)
    update_data = asset_data

    for key, value in update_data.items():
        setattr(asset, key, value)

    session.add(asset)
    session.commit()
    session.refresh(asset)
    return asset


def get_case_assets(session: Session, case_id: int) -> list[Asset]:
    stmt = (
        select(Asset)
        .where(Asset.case_id == case_id, Asset.status == AssetStatus.processed)
        .order_by(Asset.id.asc())
    )
    return session.exec(stmt).all()


def create_summary(
    session: Session, case_id: int, content: dict, url: str
) -> CaseSummary:
    new_summary = CaseSummary(
        case_id=case_id,
        content=content,
        url=url,
    )
    session.add(new_summary)
    session.commit()
    session.refresh(new_summary)
    return new_summary


def get_case_summary(session: Session, case_id: int) -> CaseSummary | None:
    stmt = select(CaseSummary).where(CaseSummary.case_id == case_id)
    return session.exec(stmt).first()
