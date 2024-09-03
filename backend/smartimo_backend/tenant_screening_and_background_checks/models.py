from django.db import models
from core.models import Report, TimeStampedModel
from lease_rental_management.models import Tenant
from property_listing.models import PropertyOwner

class PropertyManagementCompany(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    founding_date = models.DateField(blank=True, null=True)
    bank_code = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website_link = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def create_company(self, **kwargs):
        return PropertyManagementCompany.objects.create(**kwargs)

    def update_company(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()
        return self

    def delete_company(self):
        self.delete()

    def get_company(self):
        return {
            'name': self.name,
            'founding_date': self.founding_date,
            'bank_code': self.bank_code,
            'description': self.description,
            'email': self.email,
            'website_link': self.website_link,
            'phone_number': self.phone_number,
            'location': self.location,
        }

class ScreeningTenant(Tenant):
    consent_status = models.BooleanField(default=False, blank=True, null=True)
    application_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def apply_for_rental(self, name, email, phone_number, address):
        self.username = name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.application_status = "approved"
        self.save()

    def provide_consent(self, tenant_id):
        tenant = ScreeningTenant.objects.get(id=tenant_id)
        tenant.consent_status = True
        tenant.save()

    def update_application_status(self, tenant_id, status):
        tenant = ScreeningTenant.objects.get(id=tenant_id)
        tenant.application_status = status
        tenant.save()

class BackgroundCheck(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    credit_report = models.TextField(blank=True, null=True)
    criminal_record = models.TextField(blank=True, null=True)
    eviction_record = models.TextField(blank=True, null=True)
    rental_references = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')

    def initiate_check(self, tenant_id, owner_id):
        tenant = Tenant.objects.get(id=tenant_id)
        owner = PropertyOwner.objects.get(id=owner_id)
        background_check = BackgroundCheck.objects.create(
            tenant=tenant,
            owner=owner,
            status='pending'
        )
        return background_check

    def update_check_status(self, check_id, status):
        background_check = BackgroundCheck.objects.get(id=check_id)
        background_check.status = status
        background_check.save()

    def get_check_results(self, check_id):
        background_check = BackgroundCheck.objects.get(id=check_id)
        return {
            'credit_report': background_check.credit_report,
            'criminal_record': background_check.criminal_record,
            'eviction_record': background_check.eviction_record,
            'rental_references': background_check.rental_references,
            "status": background_check.status
        }

class ScreeningService(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=255, blank=True, null=True)
    api_endpoint = models.URLField(blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    supported_checks = models.JSONField(blank=True, null=True)

    def send_check_request(self, service_id, tenant_details, check_types):
        service = ScreeningService.objects.get(id=service_id)
        response = self.api_request(service.api_endpoint, tenant_details, check_types)
        return response

    def receive_check_results(self, service_id, check_id):
        service = ScreeningService.objects.get(id=service_id)
        pass

    def verify_compliance(self, service_id):
        service = ScreeningService.objects.get(id=service_id)
        pass

class ScreeningTenantPortal(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    consent_form = models.TextField(blank=True, null=True)
    application_form = models.TextField(blank=True, null=True)
    notifications = models.JSONField(blank=True, null=True)
    document_uploads = models.JSONField(blank=True, null=True)

    def submit_application_form(self, tenant_id, application_details):
        tenant_portal = ScreeningTenantPortal.objects.get(tenant_id=tenant_id)
        tenant_portal.application_form = application_details
        tenant_portal.save()

    def provide_consent(self, tenant_id, consent_status):
        tenant_portal = ScreeningTenantPortal.objects.get(tenant_id=tenant_id)
        tenant_portal.consent_form = consent_status
        tenant_portal.save()

    def upload_documents(self, tenant_id, documents):
        tenant_portal = ScreeningTenantPortal.objects.get(tenant_id=tenant_id)
        tenant_portal.document_uploads = documents
        tenant_portal.save()

    def receive_notifications(self, tenant_id):
        tenant_portal = ScreeningTenantPortal.objects.get(tenant_id=tenant_id)
        return tenant_portal.notifications

class ScreeningReport(Report):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    credit_score = models.IntegerField(blank=True, null=True)
    criminal_summary = models.TextField(blank=True, null=True)
    eviction_summary = models.TextField(blank=True, null=True)
    reference_verification = models.TextField(blank=True, null=True)
    risk_assessment = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)

    def generate_report(self, check_id):
        background_check = BackgroundCheck.objects.get(id=check_id)
        return ScreeningReport.objects.create(
            tenant=background_check.tenant,
            owner=background_check.owner,
            credit_score=background_check.credit_report,  
            criminal_summary=background_check.criminal_record, 
            eviction_summary=background_check.eviction_record,
            reference_verification=background_check.rental_references,
            risk_assessment="Assess risk based on reports",
            recommendations="Recommendations based on risk assessment"
        )

    def get_report_details(self, report_id):

        report = ScreeningReport.objects.get(id=report_id)
        return {
            'credit_score': report.credit_score,
            'criminal_summary': report.criminal_summary,
            'eviction_summary': report.eviction_summary,
            'reference_verification': report.reference_verification,
            'risk_assessment': report.risk_assessment,
            'recommendations': report.recommendations
        }

    def share_report(self, report_id):
        report = ScreeningReport.objects.get(id=report_id)
        pass

class ScreeningWorkflow(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    criteria = models.JSONField(blank=True, null=True)
    decision_rules = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    log = models.JSONField(blank=True, null=True)

    def configure_workflow(self, owner_id, criteria, decision_rules):
        return ScreeningWorkflow.objects.create(
            owner_id=owner_id,
            criteria=criteria,
            decision_rules=decision_rules,
            status='active',
            log=[]
        )

    def trigger_workflow(self, tenant_id, property_id):
        workflow = ScreeningWorkflow.objects.get(owner_id=tenant_id)
        pass

    def update_workflow(self, workflow_id, criteria=None, decision_rules=None, status=None, log=None):
        workflow = ScreeningWorkflow.objects.get(workflow_id=workflow_id)
        if criteria:
            workflow.criteria = criteria
        if decision_rules:
            workflow.decision_rules = decision_rules
        if status:
            workflow.status = status
        if log:
            workflow.log = log
        workflow.save()
        return workflow

    def track_workflow_activities(self, workflow_id):
        workflow = ScreeningWorkflow.objects.get(id=workflow_id)
        return workflow.log


class PropertyManagementPackage(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(PropertyManagementCompany, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=255, blank=True, null=True)
    screening_modules = models.JSONField(blank=True, null=True)
    branding_options = models.JSONField(blank=True, null=True)
    pricing_options = models.JSONField(blank=True, null=True)

    def create_package(self, company_id, package_name, screening_modules, branding_options, pricing_options):
        return PropertyManagementPackage.objects.create(
            company=company_id,
            package_name=package_name,
            screening_modules=screening_modules,
            branding_options=branding_options,
            pricing_options=pricing_options
        )

    def update_package(self, package_id, screening_modules, branding_options, pricing_options):
        package = PropertyManagementPackage.objects.get(id=package_id)
        package.screening_modules = screening_modules
        package.branding_options = branding_options
        package.pricing_options = pricing_options
        package.save()

    def get_package_details(self, package_id):
        package = PropertyManagementPackage.objects.get(id=package_id)
        return {
            'company_name': package.company,
            'package_name': package.package_name,
            'screening_modules': package.screening_modules,
            'branding_options': package.branding_options,
            'pricing_options': package.pricing_options
        }

