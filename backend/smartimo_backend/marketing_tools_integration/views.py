from ninja import Router
from typing import List
from .models import MarketingProperty, ListingDistribution, SocialMediaPost, AdvertisingCampaign, MarketingAnalytics
from .schemas import (MarketingPropertySchema, ListingDistributionSchema, SocialMediaPostSchema, 
                      AdvertisingCampaignSchema, MarketingAnalyticsSchema)

router = Router()

@router.post("/create-listing", response=MarketingPropertySchema)
def create_listing(request, payload: MarketingPropertySchema):
    # Logic to create a new property listing
    listing = MarketingProperty.objects.create(**payload.dict(exclude={'id'}))
    return listing

@router.post("/upload-media/{listing_id}", response=MarketingPropertySchema)
def upload_media(request, listing_id: int):
    # Logic to upload media to the listing
    listing = MarketingProperty.objects.get(id=listing_id)
    # listing.upload_media()  # Implement media upload logic here
    return listing

@router.post("/distribute-listing", response=ListingDistributionSchema)
def distribute_listing(request, payload: ListingDistributionSchema):
    distribution = ListingDistribution.objects.create(**payload.dict(exclude={'id'}))
    # distribution.distribute_listing()  # Implement distribution logic here
    return distribution

@router.post("/create-social-media-post", response=SocialMediaPostSchema)
def create_social_media_post(request, payload: SocialMediaPostSchema):
    post = SocialMediaPost.objects.create(**payload.dict(exclude={'id'}))
    # post.create_post()  # Implement social media post logic here
    return post

@router.post("/launch-ad-campaign", response=AdvertisingCampaignSchema)
def launch_ad_campaign(request, payload: AdvertisingCampaignSchema):
    campaign = AdvertisingCampaign.objects.create(**payload.dict(exclude={'id'}))
    # campaign.launch_campaign()  # Implement ad campaign launch logic here
    return campaign

@router.get("/analytics/{property_id}", response=List[MarketingAnalyticsSchema])
def get_analytics(request, property_id: int):
    analytics = MarketingAnalytics.objects.filter(property_id=property_id)
    return analytics

