from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users
from uvicorn import run

app = FastAPI(docs_url='/api/v1/docs', redoc_url='/api/v1/redoc')
app.include_router(users.router, prefix="/api/v1/users_control_service")

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
