from urllib.request import Request

from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse

from src.api.routers.login_router import login_router


@login_router.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
