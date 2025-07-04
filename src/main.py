from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.db import create_all_tables



app = FastAPI(lifespan=create_all_tables)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"message": "Server is running"}