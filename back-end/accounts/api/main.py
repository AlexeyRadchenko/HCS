from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import accounts


app = FastAPI(
    servers=[ 
        {"url": "https://komfort-trg.fvds.ru", "description": "Production environment"},
    ], 
    title='accounts service API',
    docs_url='/api/v1/accounts_service/docs', 
    redoc_url='/api/v1/accounts_service/redoc',
    openapi_url='/api/v1/accounts_service/openapi.json',
)

app.include_router(accounts.router, prefix="/api/v1/accounts_service")

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