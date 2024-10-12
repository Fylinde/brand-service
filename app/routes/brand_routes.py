from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.brand_schemas import BrandCreate, BrandUpdate, Brand
from app.crud import brand_crud
from typing import List, Optional
from app.utils.rabbitmq import RabbitMQConnection

router = APIRouter()



# RabbitMQ setup (this can be done globally in your app)
rabbitmq = RabbitMQConnection(exchange_name="brand_events", exchange_type="fanout")


# Get a brand by its ID
@router.get("/{brand_id}", response_model=Brand)
def get_brand_by_id(brand_id: int, db: Session = Depends(get_db)):
    return brand_crud.get_brand_by_id(db, brand_id)

# Get all brands with optional pagination and filtering by status
@router.get("/", response_model=List[Brand])
def get_all_brands(
    db: Session = Depends(get_db),
    skip: int = Query(0, description="Number of brands to skip for pagination"),
    limit: int = Query(10, description="Maximum number of brands to return"),
    status: Optional[bool] = Query(None, description="Filter brands by status (active/inactive)")
):
    return brand_crud.get_all_brands(db, skip=skip, limit=limit, status=status)

# Create a new brand and publish an event
@router.post("/", response_model=Brand, status_code=201)
def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    new_brand = brand_crud.create_brand(db, brand)
    
    # Publish event to RabbitMQ
    event = {
        "event": "brand_created",
        "brand_id": new_brand.id,
        "brand_name": new_brand.name,
        "description": new_brand.description
    }
    rabbitmq.publish_message(event)
    
    return new_brand

# Update a brand and publish an event
@router.put("/{brand_id}", response_model=Brand)
def update_brand(brand_id: int, brand_update: BrandUpdate, db: Session = Depends(get_db)):
    updated_brand = brand_crud.update_brand(db, brand_id, brand_update)
    
    # Publish event to RabbitMQ
    event = {
        "event": "brand_updated",
        "brand_id": updated_brand.id,
        "brand_name": updated_brand.name,
        "description": updated_brand.description,
        "status": updated_brand.status
    }
    rabbitmq.publish_message(event)
    
    return updated_brand

# Soft delete a brand and publish an event
@router.delete("/{brand_id}")
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    result = brand_crud.delete_brand(db, brand_id)
    
    # Publish event to RabbitMQ
    event = {
        "event": "brand_deleted",
        "brand_id": brand_id
    }
    rabbitmq.publish_message(event)
    
    return result

# Activate a brand and publish an event
@router.patch("/{brand_id}/activate")
def activate_brand(brand_id: int, db: Session = Depends(get_db)):
    result = brand_crud.activate_brand(db, brand_id)
    
    # Publish event to RabbitMQ
    event = {
        "event": "brand_activated",
        "brand_id": brand_id
    }
    rabbitmq.publish_message(event)
    
    return result

# Deactivate a brand and publish an event
@router.patch("/{brand_id}/deactivate")
def deactivate_brand(brand_id: int, db: Session = Depends(get_db)):
    result = brand_crud.deactivate_brand(db, brand_id)
    
    # Publish event to RabbitMQ
    event = {
        "event": "brand_deactivated",
        "brand_id": brand_id
    }
    rabbitmq.publish_message(event)
    
    return result