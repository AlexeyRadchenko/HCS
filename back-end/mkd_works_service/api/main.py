from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import mkd_works



app = FastAPI(
    servers=[ 
        {"url": "https://komfort-trg.fvds.ru", "description": "Production environment"},
    ],
    title='MKD works service API',
    docs_url='/api/v1/mkd_works_service/docs', 
    redoc_url='/api/v1/mkd_works_service/redoc',
    openapi_url='/api/v1/mkd_works_service/openapi.json',
)

app.include_router(mkd_works.router, prefix="/api/v1/mkd_works_service")

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