# from ninja import Router
# from .models import LeaseRentalAgreement, RentalPayment, LeaseRentalCommunication
# from .schemas import (
#     LeaseRentalAgreementSchema, CreateLeaseRentalAgreementSchema, UpdateLeaseRentalAgreementSchema, RentalPaymentSchema, CreateRentalPaymentSchema,
#     LeaseRentalCommunicationSchema
# )
# from django.shortcuts import get_object_or_404


# router = Router()

# @router.post("/lease-agreements/", response=LeaseRentalAgreementSchema)
# def create_lease_agreement(request, data: CreateLeaseRentalAgreementSchema):
#     lease_agreement_data = data.dict(exclude={'id'})
#     lease_agreement = LeaseRentalAgreement.objects.create(**lease_agreement_data)
#     return lease_agreement

# @router.put("/lease-agreements/{lease_agreement_id}/", response=LeaseRentalAgreementSchema)
# def update_lease_agreement(request, lease_agreement_id: int, data: UpdateLeaseRentalAgreementSchema):
#     lease_agreement = get_object_or_404(LeaseRentalAgreement, id=lease_agreement_id)
#     for attr, value in data.dict().items():
#         if attr != 'id':
#             setattr(lease_agreement, attr, value)
#     lease_agreement.save()
#     return lease_agreement

# @router.post("/rental-payments/", response=RentalPaymentSchema)
# def make_payment(request, data: CreateRentalPaymentSchema):
#     payment_data = data.dict(exclude={'id'})
#     payment = RentalPayment.objects.create(**payment_data)
#     return payment

# @router.get("/rental-payments/{payment_id}/", response=RentalPaymentSchema)
# def get_payment_status(request, payment_id: int):
#     payment = get_object_or_404(RentalPayment, id=payment_id)
#     return payment

# @router.get("/lease-rental-communications/{communication_id}/", response=LeaseRentalCommunicationSchema)
# def get_messages(request, communication_id: int):
#     communication = get_object_or_404(LeaseRentalCommunication, id=communication_id)
#     return communication

# @router.post("/lease-rental-communications/", response=LeaseRentalCommunicationSchema)
# def log_communication(request, data: LeaseRentalCommunicationSchema):
#     communication_data = data.dict(exclude={'id'})
#     communication = LeaseRentalCommunication.objects.create(**communication_data)
#     return communication

