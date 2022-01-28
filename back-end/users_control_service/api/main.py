from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users


app = FastAPI(root_path="/api/v1")
app.include_router(users.router, prefix="/users_control_service")

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

