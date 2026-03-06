import time
import logging

import psycopg2

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, OperationalError

from core.database import SQLModel, engine
from core.exceptions import AppException
from routes.auth_routes import router as AUTH_ROUTER
from routes.case_routes import router as CASE_ROUTER
from routes.user_routes import router as USER_ROUTER
from schemas.error_schemas import ErrorResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = ["http://localhost:3000", "https://casebot-q1hx.vercel.app/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AUTH_ROUTER, prefix="/api/v1/auth", tags=["auth"])
app.include_router(USER_ROUTER, prefix="/api/v1/users", tags=["users"])
app.include_router(CASE_ROUTER, prefix="/api/v1/cases", tags=["cases"])


def create_tables_with_retry(retries: int = 5, delay: int = 3) -> None:
    """
    Attempt to create all DB tables, retrying on connection failure.
    Railway provisions the DB asynchronously, so the app may start
    before Postgres is fully ready.
    """
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Attempting to create tables (attempt {attempt}/{retries})...")
            SQLModel.metadata.create_all(engine)
            logger.info("Tables created (or already exist). DB is ready.")
            return
        except OperationalError as e:
            logger.warning(f"DB not ready yet: {e}")
            if attempt < retries:
                logger.info(f"Retrying in {delay}s...")
                time.sleep(delay)
            else:
                logger.error("Could not connect to the database after all retries.")
                raise RuntimeError(
                    "Failed to connect to the database on startup. "
                    "Check your DATABASE_URL and that Postgres is running."
                ) from e


@app.on_event("startup")
def on_startup():
    create_tables_with_retry()


@app.exception_handler(AppException)
def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            message=exc.message,
        ).model_dump(),
    )


@app.exception_handler(IntegrityError)
def handle_unique_constraint_error(request: Request, exc: IntegrityError):
    if isinstance(exc.orig, psycopg2.errors.UniqueViolation):
        # Safely extract field name — guard against unexpected constraint name formats
        constraint_name = exc.orig.diag.constraint_name or ""
        parts = constraint_name.split("_")
        field_name = parts[1] if len(parts) > 1 else constraint_name
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                message=f"{field_name} already exists",
            ).model_dump(),
        )
    logger.error(f"Unhandled IntegrityError: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            message="Database integrity error",
        ).model_dump(),
    )


@app.exception_handler(OperationalError)
def handle_db_connection_error(request: Request, exc: OperationalError):
    logger.error(f"Database connection error during request: {exc}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=ErrorResponse(
            message="Database is unavailable. Please try again shortly.",
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = "Validation errors:"
    for error in exc.errors():
        # Guard against missing 'loc' fields (e.g. body-level errors)
        loc = error.get("loc", [])
        field = loc[1] if len(loc) > 1 else loc[0] if loc else "unknown"
        message += f" Field: {field}, Error: {error['msg']}."
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            message=message,
        ).model_dump(),
    )
