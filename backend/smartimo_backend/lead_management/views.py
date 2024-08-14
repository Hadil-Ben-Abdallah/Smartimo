from ninja import Router
from typing import List
from.models import LeadCaptureForm, SocialMediaLead, OfflineLead, LeadAssignment, LeadCommunication, LeadNurturing
from .schemas import LeadCaptureFormSchema, SocialMediaLeadSchema, OfflineLeadSchema, LeadAssignmentSchema, LeadCommunicationSchema, LeadNurturingSchema

router = Router()

@router.get("/lead-capture-forms", response=List[LeadCaptureFormSchema])
def list_lead_capture_forms(request):
    forms = LeadCaptureForm.objects.all()
    return forms

@router.post("/lead-capture-forms", response=LeadCaptureFormSchema)
def create_lead_capture_form(request, data: LeadCaptureFormSchema):
    form_data = data.dict(exclude={'id'})
    form = LeadCaptureFormSchema(**form_data)
    return form

@router.get("/social-media-leads", response=List[SocialMediaLeadSchema])
def list_social_media_leads(request):
    social_meadia_leads = SocialMediaLead.objects.all()
    return social_meadia_leads

@router.post("/social-media-leads", response=SocialMediaLeadSchema)
def create_social_media_lead(request, data: SocialMediaLeadSchema):
    social_meadia_lead_data = data.dict(exclude={'id'})
    social_meadia_lead = SocialMediaLeadSchema(**social_meadia_lead_data)
    return social_meadia_lead

@router.get("/offline-leads", response=List[OfflineLeadSchema])
def list_offline_leads(request):
    offline_leads = OfflineLead.objects.all()
    return offline_leads

@router.post("/offline-leads", response=OfflineLeadSchema)
def create_offline_lead(request, data: OfflineLeadSchema):
    offline_lead_data = data.dict(exclude={'id'})
    offline_lead = OfflineLeadSchema(**offline_lead_data)
    return offline_lead

@router.get("/lead-assignments", response=List[LeadAssignmentSchema])
def list_lead_assignments(request):
    assignments = LeadAssignment.objects.all()
    return assignments

@router.post("/lead-assignments", response=LeadAssignmentSchema)
def create_lead_assignment(request, data: LeadAssignmentSchema):
    assignment_data = data.dict(exclude={'id'})
    assignment = LeadAssignmentSchema(**assignment_data)
    return assignment

@router.get("/lead-communications", response=List[LeadCommunicationSchema])
def list_lead_communications(request):
    communications = LeadCommunication.objects.all()
    return communications

@router.post("/lead-communications", response=LeadCommunicationSchema)
def create_lead_communication(request, data: LeadCommunicationSchema):
    communication_data = data.dict(exclude={'id'})
    communication = LeadCommunicationSchema(**communication_data)
    return communication

@router.get("/lead-nurturings", response=List[LeadNurturingSchema])
def list_lead_nurturings(request):
    nurturings = LeadNurturing.objects.all()
    return nurturings

@router.post("/lead-nurturings", response=LeadNurturingSchema)
def create_lead_nurturing(request, data: LeadNurturingSchema):
    nurturing_data = data.dict(exclude={'id'})
    nurturing = LeadNurturingSchema(**nurturing_data)
    return nurturing
