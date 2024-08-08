from ninja import Router
from typing import List
from .models import (
    MarketplacePropertyListing,
    Booking,
    Transaction,
    Availability,
    UserAccount
)
from .schemas import (
    MarketplacePropertyListingSchema,
    BookingSchema,
    TransactionSchema,
    AvailabilitySchema,
    UserAccountSchema
)

router = Router()

@router.get("/marketplace-listings", response=List[MarketplacePropertyListingSchema])
def list_marketplace_listings(request):
    listings = MarketplacePropertyListing.objects.all()
    return listings

@router.post("/marketplace-listing", response=MarketplacePropertyListingSchema)
def create_marketplace_listing(request, data: MarketplacePropertyListingSchema):
    listing_data = data.dict(exclude={'id'})
    listing = MarketplacePropertyListing.objects.create(**listing_data)
    return listing

@router.get("/bookings", response=List[BookingSchema])
def list_bookings(request):
    bookings = Booking.objects.all()
    return bookings

@router.post("/booking", response=BookingSchema)
def create_booking(request, data: BookingSchema):
    booking_data = data.dict(exclude={'id'})
    booking = Booking.objects.create(**booking_data)
    return booking

@router.get("/transactions", response=List[TransactionSchema])
def list_transactions(request):
    transactions = Transaction.objects.all()
    return transactions

@router.post("/transaction", response=TransactionSchema)
def create_transaction(request, data: TransactionSchema):
    transaction_data = data.dict(exclude={'id'})
    transaction = Transaction.objects.create(**transaction_data)
    return transaction

@router.get("/availability", response=List[AvailabilitySchema])
def list_availability(request):
    availability = Availability.objects.all()
    return availability

@router.post("/availability", response=AvailabilitySchema)
def create_availability(request, data: AvailabilitySchema):
    availability_data = data.dict(exclude={'id'})
    availability = Availability.objects.create(**availability_data)
    return availability

@router.get("/user-accounts", response=List[UserAccountSchema])
def list_user_accounts(request):
    user_accounts = UserAccount.objects.all()
    return user_accounts

@router.post("/user-account", response=UserAccountSchema)
def create_user_account(request, data: UserAccountSchema):
    user_account_data = data.dict(exclude={'id'})
    user_account = UserAccount.objects.create(**user_account_data)
    return user_account

