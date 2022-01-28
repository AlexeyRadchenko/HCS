from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import contacts


app = FastAPI(docs_url='/api/v1/docs', redoc_url='/api/v1/redoc')

app.include_router(contacts.router, prefix="/api/v1/contacts_service")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

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