import psycopg2

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from core.database import SQLModel, engine
from core.exceptions import AppException
from routes.auth_routes import router as AUTH_ROUTER
from routes.case_routes import router as CASE_ROUTER
from routes.user_routes import router as USER_ROUTER
from schemas.error_schemas import ErrorResponse

SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

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
        field_name = exc.orig.diag.constraint_name.split("_")[1]
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                message=f"{field_name} already exists",
            ).model_dump(),
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            message="Database integrity error", detail=str(exc)
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = "Validation errors:"
    for error in exc.errors():
        message += f" Field: {error['loc'][1]}, Error: {error['msg']}"
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            message=message,
        ).model_dump(),
    )
