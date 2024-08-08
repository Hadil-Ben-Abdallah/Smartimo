from ninja import Router
from typing import List
from .models import (
    CRMIntegration,
    CRMClientSync,
    CRMSalesOpportunity,
    CRMClientInteraction,
    CRMClientSegmentation,
    CRMIntegrationSettings
)
from .schemas import (
    CRMIntegrationSchema,
    CRMClientSyncSchema,
    CRMSalesOpportunitySchema,
    CRMClientInteractionSchema,
    CRMClientSegmentationSchema,
    CRMIntegrationSettingsSchema
)

router = Router()

@router.get("/crm-integrations", response=List[CRMIntegrationSchema])
def list_crm_integrations(request):
    integrations = CRMIntegration.objects.all()
    return integrations

@router.post("/crm-integration", response=CRMIntegrationSchema)
def create_crm_integration(request, data: CRMIntegrationSchema):
    integration_data = data.dict(exclude={'id'})
    integration = CRMIntegration.objects.create(**integration_data)
    return integration

@router.get("/client-syncs", response=List[CRMClientSyncSchema])
def list_client_syncs(request):
    syncs = CRMClientSync.objects.all()
    return syncs

@router.post("/client-sync", response=CRMClientSyncSchema)
def create_client_sync(request, data: CRMClientSyncSchema):
    sync_data = data.dict(exclude={'id'})
    sync = CRMClientSync.objects.create(**sync_data)
    return sync

@router.get("/sales-opportunities", response=List[CRMSalesOpportunitySchema])
def list_sales_opportunities(request):
    opportunities = CRMSalesOpportunity.objects.all()
    return opportunities

@router.post("/sales-opportunity", response=CRMSalesOpportunitySchema)
def create_sales_opportunity(request, data: CRMSalesOpportunitySchema):
    opportunity_data = data.dict(exclude={'id'})
    opportunity = CRMSalesOpportunity.objects.create(**opportunity_data)
    return opportunity

@router.get("/client-interactions", response=List[CRMClientInteractionSchema])
def list_client_interactions(request):
    interactions = CRMClientInteraction.objects.all()
    return interactions

@router.post("/client-interaction", response=CRMClientInteractionSchema)
def create_client_interaction(request, data: CRMClientInteractionSchema):
    interaction_data = data.dict(exclude={'id'})
    interaction = CRMClientInteraction.objects.create(**interaction_data)
    return interaction

@router.get("/client-segmentation", response=List[CRMClientSegmentationSchema])
def list_client_segmentation(request):
    segments = CRMClientSegmentation.objects.all()
    return segments

@router.post("/client-segmentation", response=CRMClientSegmentationSchema)
def create_client_segmentation(request, data: CRMClientSegmentationSchema):
    segment_data = data.dict(exclude={'id'})
    segment = CRMClientSegmentation.objects.create(**segment_data)
    return segment

@router.get("/crm-integration-settings", response=List[CRMIntegrationSettingsSchema])
def list_crm_integration_settings(request):
    settings = CRMIntegrationSettings.objects.all()
    return settings

@router.post("/crm-integration-settings", response=CRMIntegrationSettingsSchema)
def create_crm_integration_settings(request, data: CRMIntegrationSettingsSchema):
    settings_data = data.dict(exclude={'id'})
    settings = CRMIntegrationSettings.objects.create(**settings_data)
    return settings


