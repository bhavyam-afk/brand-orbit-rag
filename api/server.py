from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Influencer Search Engine"
)

app.include_router(router)