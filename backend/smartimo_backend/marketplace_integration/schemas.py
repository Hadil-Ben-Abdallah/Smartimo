from ninja import Schema
from datetime import date
from pydantic import BaseModel, Field
from typing import List,  Optional
from property_listing.schemas import ThePropertyListingSchema

class MarketplacePropertyListingSchema(ThePropertyListingSchema):
    marketplace_id: str = None

    class Config:
        from_attributes = True
        populate_by_name = True

class BookingSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    user_id: int
    start_date: date
    end_date: date
    status: str
    marketplace_booking_id: str = None

    class Config:
        from_attributes = True
        populate_by_name = True

class TransactionSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    marketplace_property_listing_id: int
    amount: float
    commission: float
    date: date
    status: str
    marketplace_transaction_id: str = None

    class Config:
        from_attributes = True
        populate_by_name = True

class AvailabilitySchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    property_id: int
    availability_dates: List[date]
    price: float

    class Config:
        from_attributes = True
        populate_by_name = True

class UserAccountSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    user_id: int
    password: str
    marketplace_user_id: str = None

    class Config:
        from_attributes = True
        populate_by_name = True

