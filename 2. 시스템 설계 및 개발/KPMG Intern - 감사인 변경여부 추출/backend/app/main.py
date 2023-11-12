from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from app.routers.user_router import router as user_router
from app.routers.starred_router import router as starred_router
from app.routers.contact_router import router as contact_router
from app.routers.info_router import router as info_router
from app.routers.analysis_router import router as analysis_router
from app.database import models
from app.database.session import db_engine

models.Base.metadata.create_all(bind=db_engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

app.include_router(user_router, prefix="/user")
app.include_router(starred_router, prefix="/starred")
app.include_router(contact_router, prefix="/contact")
app.include_router(info_router, prefix="/info")
app.include_router(analysis_router, prefix="/analysis")