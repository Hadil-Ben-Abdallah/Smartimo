from ninja import Router
from typing import List
from .models import RegulationRepository, LegalDocumentGenerator, ComplianceCalendar, DueDiligenceChecker, FairHousingCompliance
from .schemas import RegulationRepositorySchema, LegalDocumentGeneratorSchema, ComplianceCalendarSchema, DueDiligenceCheckerSchema, FairHousingComplianceSchema

router = Router()

@router.get("/regulations", response=List[RegulationRepositorySchema])
def list_regulations(request, location: str = None, property_type: str = None, category: str = None):
    regulations = RegulationRepository().search_regulations(location, property_type, category)
    return regulations

@router.post("/regulations", response=RegulationRepositorySchema)
def create_regulation(request, payload: RegulationRepositorySchema):
    regulation_instance = RegulationRepository.objects.create(**payload.dict(exclude={'id'}))
    return regulation_instance.store_regulation()

@router.post("/regulations/notify", response=str)
def notify_regulation_updates(request, regulation_id: int):
    regulation = RegulationRepository.objects.get(id=regulation_id)
    return regulation.notify_updates()

@router.post("/documents/generate", response=LegalDocumentGeneratorSchema)
def generate_document(request, payload: LegalDocumentGeneratorSchema):
    doc = LegalDocumentGenerator.objects.create(**payload.dict(exclude={'id'}))
    return doc.generate_document()

@router.post("/documents/customize", response=str)
def customize_document(request, document_id: int, property_details: dict, transaction_details: dict):
    doc = LegalDocumentGenerator.objects.get(id=document_id)
    return doc.customize_document(property_details, transaction_details)

@router.post("/documents/signatures", response=str)
def manage_signatures(request, document_id: int, signatures: dict):
    doc = LegalDocumentGenerator.objects.get(id=document_id)
    return doc.manage_signatures(signatures)

@router.post("/calendar/events", response=ComplianceCalendarSchema)
def add_compliance_event(request, payload: ComplianceCalendarSchema):
    event_instance = ComplianceCalendar.objects.create(**payload.dict(exclude={'id'}))
    return event_instance.add_event(payload.event_id, payload.compliance_task)

@router.post("/calendar/reminders", response=str)
def set_reminders(request, calendar_id: int, reminders: List[str]):
    calendar = ComplianceCalendar.objects.get(id=calendar_id)
    return calendar.set_reminders(reminders)

@router.get("/calendar/deadlines", response=str)
def track_compliance_deadlines(request, calendar_id: int):
    calendar = ComplianceCalendar.objects.get(id=calendar_id)
    return calendar.track_deadlines()

@router.post("/due-diligence/check", response=DueDiligenceCheckerSchema)
def perform_due_diligence_check(request, payload: DueDiligenceCheckerSchema):
    checker = DueDiligenceChecker.objects.create(**payload.dict(exclude={'id'}))
    return checker.perform_check(payload.check_type)

@router.get("/due-diligence/reports", response=DueDiligenceCheckerSchema)
def access_due_diligence_reports(request, checker_id: int):
    checker = DueDiligenceChecker.objects.get(id=checker_id)
    return checker.access_reports()

@router.post("/due-diligence/share", response=str)
def share_due_diligence_findings(request, checker_id: int, stakeholders: List[str]):
    checker = DueDiligenceChecker.objects.get(id=checker_id)
    return checker.share_findings(stakeholders)

@router.get("/fair-housing/training", response=FairHousingComplianceSchema)
def access_fair_housing_training(request, compliance_id: int):
    compliance = FairHousingCompliance.objects.get(id=compliance_id)
    return compliance.access_training()

@router.post("/fair-housing/evaluate", response=str)
def evaluate_fair_housing_compliance(request, compliance_id: int, property_listing: str):
    compliance = FairHousingCompliance.objects.get(id=compliance_id)
    return compliance.evaluate_compliance(property_listing)

@router.get("/fair-housing/report", response=FairHousingComplianceSchema)
def generate_fair_housing_report(request, compliance_id: int):
    compliance = FairHousingCompliance.objects.get(id=compliance_id)
    return compliance.generate_report()
