from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.brand_model import BrandModel
from app.schemas.brand_schemas import BrandCreate, BrandUpdate
from fastapi import HTTPException
from datetime import datetime
from typing import List, Optional

# Create a new brand
def create_brand(db: Session, brand: BrandCreate):
    try:
        # Check if the brand already exists
        existing_brand = db.query(BrandModel).filter(BrandModel.name == brand.name).first()
        if existing_brand:
            raise HTTPException(status_code=400, detail="Brand with this name already exists.")
        
        # Create a new brand
        new_brand = BrandModel(**brand.dict())
        db.add(new_brand)
        db.commit()
        db.refresh(new_brand)
        return new_brand
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create brand") from e

# Get a brand by ID
def get_brand_by_id(db: Session, brand_id: int) -> BrandModel:
    brand = db.query(BrandModel).filter(BrandModel.id == brand_id, BrandModel.deleted_at == None).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

# Get all brands with pagination and filtering by status
def get_all_brands(
    db: Session, 
    skip: int = 0, 
    limit: int = 10, 
    status: Optional[bool] = None
) -> List[BrandModel]:
    query = db.query(BrandModel).filter(BrandModel.deleted_at == None)

    # Filter by status if provided
    if status is not None:
        query = query.filter(BrandModel.status == status)

    # Apply pagination
    return query.offset(skip).limit(limit).all()

# Update an existing brand
def update_brand(db: Session, brand_id: int, brand_update: BrandUpdate):
    brand = get_brand_by_id(db, brand_id)
    
    for key, value in brand_update.dict(exclude_unset=True).items():
        setattr(brand, key, value)

    db.commit()
    db.refresh(brand)
    return brand

# Soft delete a brand (mark it as deleted)
def delete_brand(db: Session, brand_id: int):
    brand = get_brand_by_id(db, brand_id)
    
    # Mark the brand as deleted instead of hard deletion
    brand.deleted_at = datetime.utcnow()
    db.commit()
    return {"message": "Brand has been soft deleted"}

# Activate a brand
def activate_brand(db: Session, brand_id: int):
    brand = get_brand_by_id(db, brand_id)
    if brand.status:
        raise HTTPException(status_code=400, detail="Brand is already active")

    brand.status = True
    db.commit()
    return {"message": "Brand activated"}

# Deactivate a brand
def deactivate_brand(db: Session, brand_id: int):
    brand = get_brand_by_id(db, brand_id)
    if not brand.status:
        raise HTTPException(status_code=400, detail="Brand is already inactive")

    brand.status = False
    db.commit()
    return {"message": "Brand deactivated"}
