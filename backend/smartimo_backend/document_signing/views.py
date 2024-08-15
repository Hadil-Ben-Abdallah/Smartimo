from ninja import Router
from typing import List
from .models import SigningDocument, Signer, SigningNotification, Compliance, SignatureTracker
from .schemas import SigningDocumentSchema, SignerSchema, SigningNotificationSchema, ComplianceSchema, SignatureTrackerSchema

router = Router()

@router.get("/signing-documents", response=List[SigningDocumentSchema])
def list_signing_documents(request):
    signing_documents = SigningDocument.objects.all()
    return signing_documents

@router.post("/signing-documents", response=SigningDocumentSchema)
def create_signing_document(request, data: SigningDocumentSchema):
    signing_document_data = data.dict(exclude={'id'})
    signing_document = SigningDocument.objects.create(**signing_document_data)
    return signing_document

@router.get("/signers", response=List[SignerSchema])
def list_signers(request):
    signers = Signer.objects.all()
    return signers

@router.post("/signers", response=SignerSchema)
def create_signer(request, data: SignerSchema):
    signer_data = data.dict(exclude={'id'})
    signer = Signer.objects.create(**signer_data)
    return signer

@router.get("/signing-notifications", response=List[SigningNotificationSchema])
def list_signing_notifications(request):
    signing_notifications = SigningNotification.objects.all()
    return signing_notifications

@router.post("/signing-notifications", response=SigningNotificationSchema)
def create_signing_notification(request, data: SigningNotificationSchema):
    signing_notification_data = data.dict(exclude={'id'})
    signing_notification = SigningNotification.objects.create(**signing_notification_data)
    return signing_notification

@router.get("/compliances", response=List[ComplianceSchema])
def list_compliances(request):
    compliances = Compliance.objects.all()
    return compliances

@router.post("/compliances", response=ComplianceSchema)
def create_compliance(request, data: ComplianceSchema):
    compliance_data = data.dict(exclude={'id'})
    compliance = Compliance.objects.create(**compliance_data)
    return compliance

@router.get("/signature-trackers", response=List[SignatureTrackerSchema])
def list_signature_trackers(request):
    signature_trackers = SignatureTracker.objects.all()
    return signature_trackers

@router.post("/signature-trackers", response=SignatureTrackerSchema)
def create_signature_tracker(request, data: SignatureTrackerSchema):
    signature_tracker_data = data.dict(exclude={'id'})
    signature_tracker = SignatureTracker.objects.create(**signature_tracker_data)
    return signature_tracker

