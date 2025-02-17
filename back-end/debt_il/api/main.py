from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import debt_il



app = FastAPI(
    title='Debt IL service API',
    docs_url='/api/v1/debt_il_service/docs', 
    redoc_url='/api/v1/debt_il_service/redoc',
    openapi_url='/api/v1/debt_il_service/openapi.json',
)

origins = ['komfortservices.fvds.ru', 'localhost:5173', '127.0.0.1:8060', 'http://localhost:5173']
#origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)     

app.include_router(debt_il.router, prefix="/api/v1/debt_il_service")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
