from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Email, CommunicationNotification, InstantMessage, SMSNotification, CommunicationLog
from .schemas import EmailSchema, CommunicationNotificationSchema, InstantMessageSchema, SMSNotificationSchema, CommunicationLogSchema

router = Router()

# Email Views
@router.post("/emails/", response=EmailSchema)
def create_email(request, payload: EmailSchema):
    email = Email(**payload.dict(exclude_unset=True))
    email.save()
    return email

@router.put("/emails/{email_id}/", response=EmailSchema)
def update_email(request, email_id: int, payload: EmailSchema):
    email = get_object_or_404(Email, id=email_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(email, attr, value)
    email.save()
    return email

@router.get("/emails/", response=list[EmailSchema])
def list_emails(request):
    emails = Email.objects.all()
    return emails

@router.get("/emails/{email_id}/", response=EmailSchema)
def get_email(request, email_id: int):
    email = get_object_or_404(Email, id=email_id)
    return email

@router.delete("/emails/{email_id}/")
def delete_email(request, email_id: int):
    email = get_object_or_404(Email, id=email_id)
    email.delete()
    return {"success": True}

# CommunicationNotification Views
@router.post("/notifications/", response=CommunicationNotificationSchema)
def create_notification(request, payload: CommunicationNotificationSchema):
    notification = CommunicationNotification(**payload.dict(exclude_unset=True))
    notification.save()
    return notification

@router.put("/notifications/{notification_id}/", response=CommunicationNotificationSchema)
def update_notification(request, notification_id: int, payload: CommunicationNotificationSchema):
    notification = get_object_or_404(CommunicationNotification, id=notification_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(notification, attr, value)
    notification.save()
    return notification

@router.get("/notifications/", response=list[CommunicationNotificationSchema])
def list_notifications(request):
    notifications = CommunicationNotification.objects.all()
    return notifications

@router.get("/notifications/{notification_id}/", response=CommunicationNotificationSchema)
def get_notification(request, notification_id: int):
    notification = get_object_or_404(CommunicationNotification, id=notification_id)
    return notification

@router.delete("/notifications/{notification_id}/")
def delete_notification(request, notification_id: int):
    notification = get_object_or_404(CommunicationNotification, id=notification_id)
    notification.delete()
    return {"success": True}

# InstantMessage Views
@router.post("/instant-messages/", response=InstantMessageSchema)
def create_instant_message(request, payload: InstantMessageSchema):
    message = InstantMessage(**payload.dict(exclude_unset=True))
    message.save()
    return message

@router.put("/instant-messages/{message_id}/", response=InstantMessageSchema)
def update_instant_message(request, message_id: int, payload: InstantMessageSchema):
    message = get_object_or_404(InstantMessage, id=message_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(message, attr, value)
    message.save()
    return message

@router.get("/instant-messages/", response=list[InstantMessageSchema])
def list_instant_messages(request):
    messages = InstantMessage.objects.all()
    return messages

@router.get("/instant-messages/{message_id}/", response=InstantMessageSchema)
def get_instant_message(request, message_id: int):
    message = get_object_or_404(InstantMessage, id=message_id)
    return message

@router.delete("/instant-messages/{message_id}/")
def delete_instant_message(request, message_id: int):
    message = get_object_or_404(InstantMessage, id=message_id)
    message.delete()
    return {"success": True}

# SMSNotification Views
@router.post("/sms-notifications/", response=SMSNotificationSchema)
def create_sms_notification(request, payload: SMSNotificationSchema):
    sms = SMSNotification(**payload.dict(exclude_unset=True))
    sms.save()
    return sms

@router.put("/sms-notifications/{sms_id}/", response=SMSNotificationSchema)
def update_sms_notification(request, sms_id: int, payload: SMSNotificationSchema):
    sms = get_object_or_404(SMSNotification, id=sms_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(sms, attr, value)
    sms.save()
    return sms

@router.get("/sms-notifications/", response=list[SMSNotificationSchema])
def list_sms_notifications(request):
    sms_notifications = SMSNotification.objects.all()
    return sms_notifications

@router.get("/sms-notifications/{sms_id}/", response=SMSNotificationSchema)
def get_sms_notification(request, sms_id: int):
    sms = get_object_or_404(SMSNotification, id=sms_id)
    return sms

@router.delete("/sms-notifications/{sms_id}/")
def delete_sms_notification(request, sms_id: int):
    sms = get_object_or_404(SMSNotification, id=sms_id)
    sms.delete()
    return {"success": True}

# CommunicationLog Views
@router.post("/communication-logs/", response=CommunicationLogSchema)
def create_communication_log(request, payload: CommunicationLogSchema):
    log = CommunicationLog(**payload.dict(exclude_unset=True))
    log.save()
    return log

@router.put("/communication-logs/{log_id}/", response=CommunicationLogSchema)
def update_communication_log(request, log_id: int, payload: CommunicationLogSchema):
    log = get_object_or_404(CommunicationLog, id=log_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr != 'id':
            setattr(log, attr, value)
    log.save()
    return log

@router.get("/communication-logs/", response=list[CommunicationLogSchema])
def list_communication_logs(request):
    logs = CommunicationLog.objects.all()
    return logs

@router.get("/communication-logs/{log_id}/", response=CommunicationLogSchema)
def get_communication_log(request, log_id: int):
    log = get_object_or_404(CommunicationLog, id=log_id)
    return log

@router.delete("/communication-logs/{log_id}/")
def delete_communication_log(request, log_id: int):
    log = get_object_or_404(CommunicationLog, id=log_id)
    log.delete()
    return {"success": True}
