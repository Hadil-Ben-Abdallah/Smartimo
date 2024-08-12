from ninja import Router
from django.shortcuts import get_object_or_404
from .models import TenantPortal, TenantNotification, TenantResource
from .schemas import (LoginSchema, TenantPortalSchema, TenantNotificationSchema, TenantResourceSchema)

router = Router()

# Portal Endpoints
@router.post("/portal/login", response=str)
def login(request, payload: LoginSchema):
    portal = TenantPortal.objects.first()
    return portal.login(payload.username, payload.password)

@router.post("/portal/logout", response=str)
def logout(request):
    portal = TenantPortal.objects.first()
    return portal.logout(request)

@router.post("/portal/", response=TenantPortalSchema)
def create_portal(request, payload: TenantPortalSchema):
    data = payload.dict(exclude={'id'})
    portal = TenantPortal.objects.create(**data)
    return portal

@router.put("/portal/{portal_id}", response=TenantPortalSchema)
def update_portal(request, portal_id: int, payload: TenantPortalSchema):
    portal = get_object_or_404(TenantPortal, id=portal_id)
    data = payload.dict()
    for key, value in data.items():
        if key != 'id':
            setattr(portal, key, value)
    portal.save()
    return portal

# TenantNotification Endpoints
@router.post("/tenant-notification/", response=TenantNotificationSchema)
def create_tenant_notification(request, payload: TenantNotificationSchema):
    data = payload.dict(exclude={'id'})
    tenant_notification = TenantNotification.objects.create(**data)
    return tenant_notification

@router.put("/tenant-notification/{notification_id}", response=TenantNotificationSchema)
def update_tenant_notification(request, notification_id: int, payload: TenantNotificationSchema):
    tenant_notification = get_object_or_404(TenantNotification, id=notification_id)
    data = payload.dict()
    for key, value in data.items():
        if key != 'id':
            setattr(tenant_notification, key, value)
    tenant_notification.save()
    return tenant_notification

# TenantResource Endpoints
@router.post("/tenant-resource/", response=TenantResourceSchema)
def create_tenant_resource(request, payload: TenantResourceSchema):
    data = payload.dict(exclude={'id'})
    tenant_resource = TenantResource.objects.create(**data)
    return tenant_resource

@router.put("/tenant-resource/{resource_id}", response=TenantResourceSchema)
def update_tenant_resource(request, resource_id: int, payload: TenantResourceSchema):
    tenant_resource = get_object_or_404(TenantResource, id=resource_id)
    data = payload.dict()
    for key, value in data.items():
        if key != 'id':
            setattr(tenant_resource, key, value)
    tenant_resource.save()
    return tenant_resource

@router.post("/tenant-resource/{resource_id}/subscribe", response=str)
def subscribe_to_updates(request, resource_id: int):
    tenant_resource = get_object_or_404(TenantResource, id=resource_id)
    return tenant_resource.subscribe_to_updates(resource_id)

@router.get("/tenant-resource/announcements", response=list)
def view_announcements(request):
    tenant_resources = TenantResource.objects.all()
    announcements = [resource.view_announcements() for resource in tenant_resources]
    return announcements

