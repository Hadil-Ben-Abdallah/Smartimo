from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Agreement, Tenant, PropertyManager, RentalPayment, LeaseRentalCommunication
from .schemas import (
    AgreementSchema, TenantSchema, PropertyManagerSchema, RentalPaymentSchema, LeaseRentalCommunicationSchema
)

router = Router()

@router.post("/agreements", response=AgreementSchema)
def create_agreement(request, payload: AgreementSchema):
    agreement = Agreement.objects.create(**payload.dict(exclude={'id'}))
    return agreement

@router.put("/agreements/{agreement_id}", response=AgreementSchema)
def update_agreement(request, agreement_id: int, payload: AgreementSchema):
    agreement = get_object_or_404(Agreement, id=agreement_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(agreement, key, value)
    agreement.save()
    return agreement

@router.post("/tenants", response=TenantSchema)
def create_tenant(request, payload: TenantSchema):
    tenant = Tenant.objects.create(**payload.dict(exclude={'id'}))
    return tenant

@router.put("/tenants/{tenant_id}", response=TenantSchema)
def update_tenant(request, tenant_id: int, payload: TenantSchema):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(tenant, key, value)
    tenant.save()
    return tenant

@router.post("/property-managers", response=PropertyManagerSchema)
def create_property_manager(request, payload: PropertyManagerSchema):
    property_manager = PropertyManager.objects.create(**payload.dict(exclude={'id'}))
    return property_manager

@router.put("/property-managers/{property_manager_id}", response=PropertyManagerSchema)
def update_property_manager(request, property_manager_id: int, payload: PropertyManagerSchema):
    property_manager = get_object_or_404(PropertyManager, id=property_manager_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(property_manager, key, value)
    property_manager.save()
    return property_manager

@router.post("/rental-payments", response=RentalPaymentSchema)
def create_rental_payment(request, payload: RentalPaymentSchema):
    rental_payment = RentalPayment.objects.create(**payload.dict(exclude={'id'}))
    return rental_payment

@router.put("/rental-payments/{rental_payment_id}", response=RentalPaymentSchema)
def update_rental_payment(request, rental_payment_id: int, payload: RentalPaymentSchema):
    rental_payment = get_object_or_404(RentalPayment, id=rental_payment_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(rental_payment, key, value)
    rental_payment.save()
    return rental_payment

@router.post("/lease-rental-communications", response=LeaseRentalCommunicationSchema)
def create_lease_rental_communication(request, payload: LeaseRentalCommunicationSchema):
    lease_rental_communication = LeaseRentalCommunication.objects.create(**payload.dict(exclude={'id'}))
    return lease_rental_communication

@router.put("/lease-rental-communications/{lease_rental_communication_id}", response=LeaseRentalCommunicationSchema)
def update_lease_rental_communication(request, lease_rental_communication_id: int, payload: LeaseRentalCommunicationSchema):
    lease_rental_communication = get_object_or_404(LeaseRentalCommunication, id=lease_rental_communication_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(lease_rental_communication, key, value)
    lease_rental_communication.save()
    return lease_rental_communication


