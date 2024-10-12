from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema for creating a new brand
class BrandCreate(BaseModel):
    name: str = Field(..., max_length=255, description="The name of the brand (max 255 characters)")
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the brand (max 500 characters)")

# Schema for updating an existing brand
class BrandUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Updated name of the brand")
    description: Optional[str] = Field(None, max_length=500, description="Updated description of the brand")
    status: Optional[bool] = Field(None, description="Set to true if the brand is active, false if inactive")

# Schema for brand representation
class Brand(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: bool  # Indicates if the brand is active
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None  # Soft deletion timestamp

    class Config:
        orm_mode = True
