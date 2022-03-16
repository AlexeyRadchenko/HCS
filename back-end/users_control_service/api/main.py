from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users
from uvicorn import run

app = FastAPI(
    title='users control API',
    docs_url='/docs', 
    redoc_url='/redoc',
    openapi_url='/openapi.json',
    root_path='/api/v1/users_control_service'
)
app.include_router(users.router)

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
