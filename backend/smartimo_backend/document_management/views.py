from ninja import Router
from django.shortcuts import get_object_or_404
from .models import (
    PropertyDocument,
    DocumentCategory,
    DocumentTag,
    DocumentExpirationReminder,
    DocumentSharing,
    ESignatureIntegration,
)
from .schemas import (
    PropertyDocumentSchema,
    DocumentCategorySchema,
    DocumentTagSchema,
    DocumentExpirationReminderSchema,
    DocumentSharingSchema,
    ESignatureIntegrationSchema,
)

router = Router()

@router.post("/documents/", response=PropertyDocumentSchema)
def upload_document(request, payload: PropertyDocumentSchema):
    document_data = payload.dict(exclude={'id'})
    document = PropertyDocument.objects.create(**document_data)
    document.upload_document(payload.file_path)
    return document

@router.put("/documents/{document_id}/", response=PropertyDocumentSchema)
def update_document(request, document_id: int, payload: PropertyDocumentSchema):
    document = get_object_or_404(PropertyDocument, id=document_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(document, key, value)
    document.save()
    return document

@router.post("/document_categories/", response=DocumentCategorySchema)
def create_category(request, payload: DocumentCategorySchema):
    category_data = payload.dict(exclude={'id'})
    category = DocumentCategory.objects.create(**category_data)
    return category

@router.put("/document_categories/{category_id}/", response=DocumentCategorySchema)
def update_category(request, category_id: int, payload: DocumentCategorySchema):
    category = get_object_or_404(DocumentCategory, id=category_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(category, key, value)
    category.save()
    return category

@router.delete("/document_categories/{category_id}/", response=dict)
def delete_category(request, category_id: int):
    category = get_object_or_404(DocumentCategory, id=category_id)
    category.delete()
    return {"success": True}

@router.post("/document_tags/", response=DocumentTagSchema)
def create_tag(request, payload: DocumentTagSchema):
    tag_data = payload.dict(exclude={'id'})
    tag = DocumentTag.objects.create(**tag_data)
    return tag

@router.put("/document_tags/{tag_id}/", response=DocumentTagSchema)
def update_tag(request, tag_id: int, payload: DocumentTagSchema):
    tag = get_object_or_404(DocumentTag, id=tag_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(tag, key, value)
    tag.save()
    return tag

@router.delete("/document_tags/{tag_id}/", response=dict)
def delete_tag(request, tag_id: int):
    tag = get_object_or_404(DocumentTag, id=tag_id)
    tag.delete()
    return {"success": True}

@router.post("/document_reminders/", response=DocumentExpirationReminderSchema)
def create_reminder(request, payload: DocumentExpirationReminderSchema):
    reminder_data = payload.dict(exclude={'id'})
    reminder = DocumentExpirationReminder.objects.create(**reminder_data)
    return reminder

@router.put("/document_reminders/{reminder_id}/", response=DocumentExpirationReminderSchema)
def update_reminder(request, reminder_id: int, payload: DocumentExpirationReminderSchema):
    reminder = get_object_or_404(DocumentExpirationReminder, id=reminder_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(reminder, key, value)
    reminder.save()
    return reminder

@router.post("/document_sharing/", response=DocumentSharingSchema)
def share_document(request, payload: DocumentSharingSchema):
    sharing_data = payload.dict(exclude={'id'})
    sharing = DocumentSharing.objects.create(**sharing_data)
    sharing.share_document(
        document_id=payload.document_id,
        shared_with=payload.shared_with,
        access_permissions=payload.access_permissions
    )
    return sharing

@router.put("/document_sharing/{sharing_id}/", response=DocumentSharingSchema)
def update_permissions(request, sharing_id: int, payload: DocumentSharingSchema):
    sharing = get_object_or_404(DocumentSharing, id=sharing_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(sharing, key, value)
    sharing.save()
    return sharing

@router.delete("/document_sharing/{sharing_id}/", response=dict)
def revoke_access(request, sharing_id: int):
    sharing = get_object_or_404(DocumentSharing, id=sharing_id)
    sharing.revoke_access()
    return {"success": True}

@router.post("/e_signature/", response=ESignatureIntegrationSchema)
def initiate_signature(request, payload: ESignatureIntegrationSchema):
    signature_data = payload.dict(exclude={'id'})
    signature = ESignatureIntegration.objects.create(**signature_data)
    signature.initiate_signature(
        document_id=payload.document_id,
        signing_party=payload.signing_party
    )
    return signature

@router.put("/e_signature/{signature_id}/", response=ESignatureIntegrationSchema)
def update_signature_status(request, signature_id: int, payload: ESignatureIntegrationSchema):
    signature = get_object_or_404(ESignatureIntegration, id=signature_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(signature, key, value)
    signature.save()
    return signature
