from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users
from uvicorn import run

app = FastAPI(
    servers=[ 
        {"url": "https://komfort-trg.fvds.ru", "description": "Production environment"},
    ], 
    title='users control API',
    docs_url='/api/v1/users_control_service/docs', 
    redoc_url='/api/v1/users_control_service/redoc',
    openapi_url='/api/v1/users_control_service/openapi.json',
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
