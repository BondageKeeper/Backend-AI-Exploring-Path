from fastapi import FastAPI , Request , status
import uvicorn
from fastapi.exceptions import RequestValidationError
from PC_Bang.app.routers import booking_storage
from PC_Bang.app.crud import engine , AlchemyLaunch , engine_session , ComputersDB
from loguru import logger
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

logger.add('Users_registration_errors.log',rotation='300 MB',retention=5,level='INFO')
app = FastAPI(title='CyberClub API')
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex = r".*",
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
app.include_router(booking_storage.router)

@app.get('/')
async def root():
    return FileResponse("frontend/main_cover.html")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,exc: RequestValidationError):
    error_details = exc.errors()
    logger.error(f'Validation failed for URL {request.url}.Errors: {error_details}')
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": error_details}
    )

from sqlalchemy import select
@app.on_event("startup")
async def start_server_task():
    async with engine.begin() as loading:
        await loading.run_sync(AlchemyLaunch.metadata.create_all)
    async with engine_session() as session:
        request = select(ComputersDB)
        result = await session.execute(request)
        existing_computers = result.scalars().all()
        if not existing_computers:
            default_models = [
                "Aspire3", "Aspire15", "MSI-Katana-01", "MSI-Katana-02",
                "ASUS-ROG-VIP1", "ASUS-ROG-VIP2", "HyperPC-Ultra",
                "Lenovo-Legion-01", "Lenovo-Legion-02", "Custom-Streamer-Box"
            ]
            for model in default_models:
                new_pc = ComputersDB(model_name = model)
                session.add(new_pc)
            await session.commit()
if __name__ == "__main__":
    uvicorn.run("PC_Bang.app.main:app",host="0.0.0.0",port=8080,reload=True)

