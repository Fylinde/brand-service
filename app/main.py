from fastapi import FastAPI
from app.database import BaseModel, engine
from app.routes import brand_routes

app = FastAPI()

# Create the database tables
#BaseModel.metadata.create_all(bind=engine)

# Include the routes
app.include_router(brand_routes.router, prefix="/brands", tags=["brands"])
