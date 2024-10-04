from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import debt_il


app = FastAPI(
    """servers=[ 
        {"url": "https://komfort-trg.fvds.ru", "description": "Production environment"},
    ],"""
    title='Debt IL service API',
    docs_url='/api/v1/debt_il_service/docs', 
    redoc_url='/api/v1/debt_il_service/redoc',
    openapi_url='/api/v1/debt_il_service/openapi.json',
)

app.include_router(debt_il.router, prefix="/api/v1/debt_il_service")

#origins = ['https://komfort-trg.fvds.ru', 'https://komfort-services.fvds.ru']
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