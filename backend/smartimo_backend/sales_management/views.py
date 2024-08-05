from ninja import Router
from .models import Lead, TheSalesOpportunity, SalesPipeline, Collaboration, SalesAnalytics, Deal
from .schemas import (
    LeadSchema, CreateLeadSchema, UpdateLeadSchema, 
    TheSalesOpportunitySchema, 
    SalesPipelineSchema, CreatePipelineSchema, UpdatePipelineSchema, 
    CollaborationSchema, 
    SalesAnalyticsSchema,
    DealSchema,
    CreateDealSchema,
    UpdateDealSchema,
)
from django.shortcuts import get_object_or_404


router = Router()

@router.post("/leads/", response=LeadSchema)
def create_lead(request, payload: CreateLeadSchema):
    lead_data = payload.dict(exclude={'id'})
    lead = Lead.objects.create(**lead_data)
    return lead

@router.put("/leads/{lead_id}/", response=LeadSchema)
def update_lead(request, lead_id: int, payload: UpdateLeadSchema):
    lead = get_object_or_404(Lead, id=lead_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id': 
            setattr(lead, attr, value)
    lead.save()
    return lead

@router.get("/leads/{lead_id}/", response=LeadSchema)
def get_lead_details(request, lead_id: int):
    lead = get_object_or_404(Lead, id=lead_id)
    return lead

@router.post("/deals/", response=DealSchema)
def create_deal(request, payload: CreateDealSchema):
    deal_data = payload.dict(exclude={'id'})
    deal = Deal.objects.create(**deal_data)
    return deal

@router.put("/deals/{deal_id}/", response=DealSchema)
def update_deal(request, deal_id: int, payload: UpdateDealSchema):
    deal = get_object_or_404(Deal, id=deal_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id': 
            setattr(deal, attr, value)
    deal.save()
    return deal

@router.get("/deals/{deal_id}/", response=DealSchema)
def get_deal_details(request, deal_id: int):
    deal = get_object_or_404(Deal, id=deal_id)
    return deal

@router.post("/sales_opportunities/", response=TheSalesOpportunitySchema)
def create_sales_opportunity(request, payload: TheSalesOpportunitySchema):
    opportunity_data = payload.dict(exclude={'id'})
    sales_opportunity = TheSalesOpportunity.objects.create(**opportunity_data)
    return sales_opportunity

@router.put("/sales_opportunities/{opportunity_id}/", response=TheSalesOpportunitySchema)
def update_sales_opportunity(request, opportunity_id: int, payload: TheSalesOpportunitySchema):
    opportunity = get_object_or_404(TheSalesOpportunity, id=opportunity_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(opportunity, attr, value)
    opportunity.save()
    return opportunity

@router.get("/sales_opportunities/{opportunity_id}/", response=TheSalesOpportunitySchema)
def get_opportunity_details(request, opportunity_id: int):
    opportunity = get_object_or_404(TheSalesOpportunity, id=opportunity_id)
    return opportunity

@router.post("/sales_pipelines/", response=SalesPipelineSchema)
def create_sales_pipeline(request, payload: CreatePipelineSchema):
    pipeline_data = payload.dict(exclude={'id'})
    pipeline = SalesPipeline.objects.create(**pipeline_data)
    return pipeline

@router.put("/sales_pipelines/{pipeline_id}/", response=SalesPipelineSchema)
def update_sales_pipeline(request, pipeline_id: int, payload: UpdatePipelineSchema):
    pipeline = get_object_or_404(SalesPipeline, id=pipeline_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(pipeline, attr, value)
    pipeline.save()
    return pipeline

@router.get("/sales_pipelines/{pipeline_id}/", response=SalesPipelineSchema)
def get_pipeline_details(request, pipeline_id: int):
    pipeline = get_object_or_404(SalesPipeline, id=pipeline_id)
    return pipeline

@router.post("/collaborations/", response=CollaborationSchema)
def add_collaboration(request, payload: CollaborationSchema):
    collaboration_data = payload.dict(exclude={'id'})
    collaboration = Collaboration.objects.create(**collaboration_data)
    return collaboration

@router.put("/collaborations/{collaboration_id}/", response=CollaborationSchema)
def update_collaboration(request, collaboration_id: int, payload: CollaborationSchema):
    collaboration = get_object_or_404(Collaboration, id=collaboration_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(collaboration, attr, value)
    collaboration.save()
    return collaboration

@router.get("/sales_analytics/{analytics_id}/", response=SalesAnalyticsSchema)
def get_sales_analytics(request, analytics_id: int):
    analytics = get_object_or_404(SalesAnalytics, id=analytics_id)
    return analytics

@router.post("/sales_analytics/", response=SalesAnalyticsSchema)
def create_sales_analytics(request, payload: SalesAnalyticsSchema):
    analytics_data = payload.dict(exclude={'id'})
    analytics = SalesAnalytics.objects.create(**analytics_data)
    return analytics

