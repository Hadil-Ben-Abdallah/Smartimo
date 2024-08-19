from ninja import Router
from typing import List
from .models import SustainabilityInitiative, SustainabilityDashboard, SustainabilityCertification, TenantSustainabilityResource, PropertySustainabilityRating, SustainabilityForum
from .schemas import SustainabilityInitiativeSchema, SustainabilityDashboardSchema, SustainabilityCertificationSchema, TenantSustainabilityResourceSchema, PropertySustainabilityRatingSchema, SustainabilityForumSchema

router = Router()

@router.get("/initiatives/", response=List[SustainabilityInitiativeSchema])
def list_initiatives(request):
    return SustainabilityInitiative.objects.all()

@router.post("/initiatives/", response=SustainabilityInitiativeSchema)
def create_initiative(request, payload: SustainabilityInitiativeSchema):
    initiative = SustainabilityInitiative.objects.create(**payload.dict(exclude={'id'}))
    return initiative

@router.put("/initiatives/{initiative_id}", response=SustainabilityInitiativeSchema)
def update_initiative(request, initiative_id: int, payload: SustainabilityInitiativeSchema):
    initiative = SustainabilityInitiative.objects.get(id=initiative_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id': 
            setattr(initiative, attr, value)
    initiative.save()
    return initiative

@router.delete("/initiatives/{initiative_id}")
def delete_initiative(request, initiative_id: int):
    initiative = SustainabilityInitiative.objects.get(id=initiative_id)
    initiative.delete()
    return {"success": True}

@router.get("/dashboards/", response=List[SustainabilityDashboardSchema])
def list_dashboards(request):
    return SustainabilityDashboard.objects.all()

@router.post("/dashboards/", response=SustainabilityDashboardSchema)
def create_dashboard(request, payload: SustainabilityDashboardSchema):
    dashboard = SustainabilityDashboard.objects.create(**payload.dict(exclude={'id'}))
    return dashboard

@router.get("/certifications/", response=List[SustainabilityCertificationSchema])
def list_certifications(request):
    return SustainabilityCertification.objects.all()

@router.post("/certifications/", response=SustainabilityCertificationSchema)
def create_certification(request, payload: SustainabilityCertificationSchema):
    certification = SustainabilityCertification.objects.create(**payload.dict(exclude={'id'}))
    return certification

@router.put("/certifications/{certification_id}", response=SustainabilityCertificationSchema)
def update_certification(request, certification_id: int, payload: SustainabilityCertificationSchema):
    certification = SustainabilityCertification.objects.get(id=certification_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id': 
            setattr(certification, attr, value)
    certification.save()
    return certification

@router.get("/resources/", response=List[TenantSustainabilityResourceSchema])
def list_resources(request):
    return TenantSustainabilityResource.objects.all()

@router.post("/resources/", response=TenantSustainabilityResourceSchema)
def create_resource(request, payload: TenantSustainabilityResourceSchema):
    resource = TenantSustainabilityResource.objects.create(**payload.dict(exclude={'id'}))
    return resource

@router.get("/ratings/", response=List[PropertySustainabilityRatingSchema])
def list_ratings(request):
    return PropertySustainabilityRating.objects.all()

@router.post("/ratings/", response=PropertySustainabilityRatingSchema)
def create_rating(request, payload: PropertySustainabilityRatingSchema):
    rating = PropertySustainabilityRating.objects.create(**payload.dict(exclude={'id'}))
    return rating

@router.get("/forums/", response=List[SustainabilityForumSchema])
def list_forums(request):
    return SustainabilityForum.objects.all()

@router.post("/forums/", response=SustainabilityForumSchema)
def create_forum(request, payload: SustainabilityForumSchema):
    forum = SustainabilityForum.objects.create(**payload.dict(exclude={'id'}))
    return forum

