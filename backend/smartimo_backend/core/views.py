from ninja import Router
from .models import Property, Notification, ClientInteraction,Communication, FinancialReport, SalesOpportunity, Resource, User, Document, Reminder, Portal, Feedback
from .schemas import PropertySchema, NotificationSchema, ClientInteractionSchema, CommunicationSchema, FinancialReportSchema, SalesOpportunitySchema, ResourceSchema, UserSchema, DocumentSchema, ReminderSchema, PortalSchema, FeedbackSchema

router = Router()

@router.get("/get-properties/", response=list[PropertySchema])
def list_properties(request):
    return list(Property.objects.all())

@router.post("/set-properties/", response=PropertySchema)
def create_property(request, data: PropertySchema):
    property_data = data.dict(exclude={'property_id'})
    property_instance = Property.objects.create(**property_data)
    return property_instance

@router.get("/get-notifications/", response=list[NotificationSchema])
def list_notifications(request):
    return list(Notification.objects.all())

@router.post("/set-notifications/", response=NotificationSchema)
def create_notification(request, data: NotificationSchema):
    notification_data = data.dict(exclude={'notification_id'})
    notification_instance = Notification.objects.create(**notification_data)
    return notification_instance

@router.get("/get-reminders/", response=list[ReminderSchema])
def list_reminders(request):
    return list(Reminder.objects.all())

@router.post("/set-reminders/", response=ReminderSchema)
def create_reminder(request, data: ReminderSchema):
    reminder_data = data.dict(exclude={'reminder_id'})
    reminder_instance = Reminder.objects.create(**reminder_data)
    return reminder_instance

@router.get("/get-client-interactions/", response=list[ClientInteractionSchema])
def list_client_interactions(request):
    return list(ClientInteraction.objects.all())

@router.post("/set-client-interactions/", response=ClientInteractionSchema)
def create_client_interaction(request, data: ClientInteractionSchema):
    client_interaction_data = data.dict(exclude={'client_interaction_id'})
    client_interaction_instance = ClientInteraction.objects.create(**client_interaction_data)
    return client_interaction_instance

@router.get("/get-communications/", response=list[CommunicationSchema])
def list_communications(request):
    return list(Communication.objects.all())

@router.post("/set-communications/", response=CommunicationSchema)
def create_communication(request, data: CommunicationSchema):
    communication_data = data.dict(exclude={'communication_id'})
    communication_instance = Communication.objects.create(**communication_data)
    return communication_instance

# @router.get("/get-lease-agreements/", response=list[LeaseAgreementSchema])
# def list_lease_agreements(request):
#     return list(LeaseAgreement.objects.all())

# @router.post("/set-lease-agreements/", response=LeaseAgreementSchema)
# def create_lease_agreement(request, data: LeaseAgreementSchema):
#     lease_agreement_data = data.dict(exclude={'lease_agreement_id'})
#     lease_agreement_instance = LeaseAgreement.objects.create(**lease_agreement_data)
#     return lease_agreement_instance

# @router.get("/get-property-listings/", response=list[PropertyListingSchema])
# def list_property_listings(request):
#     return list(PropertyListing.objects.all())

# @router.post("/set-property-listings/", response=PropertyListingSchema)
# def create_property_listing(request, data: PropertyListingSchema):
#     property_listing_data = data.dict(exclude={'property_listing_id'})
#     property_listing_instance = PropertyListing.objects.create(**property_listing_data)
#     return property_listing_instance

@router.get("/get-financial-reports/", response=list[FinancialReportSchema])
def list_financial_reports(request):
    return list(FinancialReport.objects.all())

@router.post("/set-financial-reports/", response=FinancialReportSchema)
def create_financial_report(request, data: FinancialReportSchema):
    financial_report_data = data.dict(exclude={'financial_report_id'})
    financial_report_instance = FinancialReport.objects.create(**financial_report_data)
    return financial_report_instance

@router.get("/get-sales-opportunities/", response=list[SalesOpportunitySchema])
def list_sales_opportunities(request):
    return list(SalesOpportunity.objects.all())

@router.post("/set-sales-opportunities/", response=SalesOpportunitySchema)
def create_sales_opportunity(request, data: SalesOpportunitySchema):
    sales_opportunity_data = data.dict(exclude={'sales_opportunity_id'})
    sales_opportunity_instance = SalesOpportunity.objects.create(**sales_opportunity_data)
    return sales_opportunity_instance

@router.get("/get-resources/", response=list[ResourceSchema])
def list_resources(request):
    return list(Resource.objects.all())

@router.post("/set-resources/", response=ResourceSchema)
def create_resource(request, data: ResourceSchema):
    resource_data = data.dict(exclude={'resource_id'})
    resource_instance = Resource.objects.create(**resource_data)
    return resource_instance

@router.get("/get-users/", response=list[UserSchema])
def list_users(request):
    return list(User.objects.all())

@router.post("/set-users/", response=UserSchema)
def create_user(request, data: UserSchema):
    user_data = data.dict(exclude={'user_id'})
    user_instance = User.objects.create(**user_data)
    return user_instance

@router.get("/get-documents/", response=list[DocumentSchema])
def list_documents(request):
    return list(Document.objects.all())

@router.post("/set-documents/", response=DocumentSchema)
def create_document(request, data: DocumentSchema):
    document_data = data.dict(exclude={'document_id'})
    document_instance = Document.objects.create(**document_data)
    return document_instance

@router.get("/get-portals/", response=list[PortalSchema])
def list_portals(request):
    return list(Portal.objects.all())

@router.post("/set-portals/", response=PortalSchema)
def create_portal(request, data: PortalSchema):
    portal_data = data.dict(exclude={'portal_id'})
    portal_instance = Portal.objects.create(**portal_data)
    return portal_instance

@router.get("/get-feedbacks/", response=list[FeedbackSchema])
def list_feedbacks(request):
    return list(Feedback.objects.all())

@router.post("/set-feedbacks/", response=FeedbackSchema)
def create_feedback(request, data: FeedbackSchema):
    feedback_data = data.dict(exclude={'feedback_id'})
    feedback_instance = Feedback.objects.create(**feedback_data)
    return feedback_instance
