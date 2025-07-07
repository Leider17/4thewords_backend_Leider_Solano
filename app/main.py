from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import create_all_tables
from app.routes.province_route import router as province_router
from app.routes.canton_route import router as canton_router
from app.routes.district_route import router as district_router
from app.routes.legend_route import router as legend_router
from app.routes.category_route import router as category_router
from app.routes.auth_route import router as auth_router


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

app.include_router(province_router)
app.include_router(canton_router)  
app.include_router(district_router)
app.include_router(legend_router)
app.include_router(category_router)
app.include_router(auth_router)