from ninja import Router
from typing import List
from .models import Agency, RealEstateAgent, ThePropertyListing, PropertyOwner, ProspectiveBuyerRenter, SavedListing, PropertyNotification
from .schemas import AgencySchema, RealEstateAgentSchema, ThePropertyListingSchema, PropertyOwnerSchema, ProspectiveBuyerRenterSchema, SavedListingSchema, PropertyNotificationSchema

router = Router()

@router.get("/agencies", response=List[AgencySchema])
def list_agencies(request):
    agencies = Agency.objects.all()
    return agencies

@router.get("/agents", response=List[RealEstateAgentSchema])
def list_agents(request):
    agents = RealEstateAgent.objects.all()
    return agents

@router.get("/listings", response=List[ThePropertyListingSchema])
def list_listings(request):
    listings = ThePropertyListing.objects.all()
    return listings

@router.post("/listing", response=ThePropertyListingSchema)
def create_listing(request, data: ThePropertyListingSchema):
    # Exclude 'id' field while creating
    listing_data = data.dict(exclude={'id'})
    listing = ThePropertyListing.objects.create(**listing_data)
    return listing

@router.get("/owners", response=List[PropertyOwnerSchema])
def list_owners(request):
    owners = PropertyOwner.objects.all()
    return owners

@router.get("/buyers-renters", response=List[ProspectiveBuyerRenterSchema])
def list_buyers_renters(request):
    buyers_renters = ProspectiveBuyerRenter.objects.all()
    return buyers_renters

@router.post("/save-listing", response=SavedListingSchema)
def save_listing(request, data: SavedListingSchema):
    saved_listing_data = data.dict(exclude={'id'})
    saved_listing = SavedListing.objects.create(**saved_listing_data)
    return saved_listing

@router.get("/notifications", response=List[PropertyNotificationSchema])
def list_notifications(request):
    notifications = PropertyNotification.objects.all()
    return notifications
