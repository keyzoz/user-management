import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.api.routers.login_router import login_router
from src.api.routers.user_router import user_router
from src.api.routers.users_router import users_router
from src.api.schemas import HealthCheckResponse

app = FastAPI(title="user_managment")

main_api_router = APIRouter()


main_api_router.include_router(login_router, prefix="/auth", tags=["tags"])
main_api_router.include_router(user_router, prefix="/user", tags=["tags"])
main_api_router.include_router(users_router, prefix="", tags=["tags"])

app.include_router(main_api_router)


@app.get("/healthcheck", response_model=HealthCheckResponse)
async def get_healthcheck():
    return HealthCheckResponse(status_code=200, detail="Server is up and running")


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
