from django.db import models
import datetime
from core.models import Property, TimeStampedModel
from tenant_screening_and_background_checks.models import PropertyManagementCompany

class InsurancePolicy(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    propert = models.ForeignKey(Property, on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=100, blank=True, null=True)
    coverage_type = models.CharField(max_length=100, blank=True, null=True)
    coverage_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deductible = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    premium = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    renewal_date = models.DateField(blank=True, null=True)
    insurer_contact = models.TextField(blank=True, null=True)

    def create_policy(self, property_id, policy_number, coverage_type, coverage_limit, deductible, premium, renewal_date, insurer_contact):
        return self.create(
            property=property_id,
            policy_number=policy_number,
            coverage_type=coverage_type,
            coverage_limit=coverage_limit,
            deductible=deductible,
            premium=premium,
            renewal_date=renewal_date,
            insurer_contact=insurer_contact
        )

    def update_policy(self, policy_id, policy_details):
        policy = self.get(pk=policy_id)
        for attr, value in policy_details.items():
            setattr(policy, attr, value)
        policy.save()
        return policy

    def set_renewal_reminder(self, policy_id):
        policy = self.get(pk=policy_id)
        # Setting a reminder
        return f"Reminder set for policy {policy_id} renewal on {self.renewal_date}"
    
class Incident(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    incident_details = models.TextField(blank=True, null=True)
    incident_date = models.DateField(blank=True, null=True)
    supporting_documents = models.JSONField(blank=True, null=True)

    def log_incident(self, property_id, incident_details, incident_date, supporting_documents):
        return self.create(
            property=property_id,
            incident_details=incident_details,
            incident_date=incident_date,
            supporting_documents=supporting_documents
        )

    def update_incident(self, incident_id, incident_details):
        incident = self.get(pk=incident_id)
        self.incident_details = incident_details
        incident.save()
        return incident

    def associate_claim(self, incident_id, claim_id):
        incident = self.get(pk=incident_id)
        claim = InsuranceClaim.objects.get(pk=claim_id)
        return claim

class InsuranceClaim(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    claim_details = models.TextField(blank=True, null=True)
    claim_status = models.CharField(max_length=100, choices=[('pending', 'pending'),('submitted', 'Submitted')], default='pending')
    submitted_date = models.DateField(blank=True, null=True)
    resolution_date = models.DateField(null=True, blank=True)
    claim_documents = models.JSONField(blank=True, null=True)

    def file_claim(self, property_id, policy_id, incident_id, claim_details, claim_documents):
        return self.create(
            property_id=property_id,
            policy_id=policy_id,
            incident_id=incident_id,
            claim_details=claim_details,
            claim_status="Submitted",
            submitted_date=datetime.date.today(),
            claim_documents=claim_documents
        )

    def update_claim_status(self, claim_id, claim_status):
        claim = self.get(pk=claim_id)
        self.claim_status = claim_status
        claim.save()
        return claim

    def track_claim_progress(self):
        return {
            "status": self.claim_status,
            "submitted_date": self.submitted_date,
            "resolution_date": self.resolution_date
        }


class InsuranceProvider(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    provider_name = models.CharField(max_length=200)
    contact_info = models.TextField(blank=True, null=True)
    policies = models.ManyToManyField(InsurancePolicy, related_name='providers')
    claims = models.ManyToManyField(InsuranceClaim, related_name='providers')

    def register_provider(self, provider_name, contact_info):
        return self.create(
            provider_name=provider_name,
            contact_info=contact_info
        )

    def update_provider(self, provider_id, contact_info):
        provider = self.get(pk=provider_id)
        self.contact_info = contact_info
        provider.save()
        return provider

    def offer_policy(self, provider_id, policy_details):
        provider = self.get(pk=provider_id)
        return policy_details

class InsuranceAdvisoryService(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(PropertyManagementCompany, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=200)
    advisors = models.JSONField(blank=True, null=True)
    resources = models.JSONField(blank=True, null=True)
    support_services = models.JSONField(blank=True, null=True)

    def create_advisory_service(self, company_id, service_name, advisors, resources, support_services):
        return self.create(
            company=company_id,
            service_name=service_name,
            advisors=advisors,
            resources=resources,
            support_services=support_services
        )

    def update_advisory_service(self, service_id, service_details):
        service = self.get(pk=service_id)
        for attr, value in service_details.items():
            setattr(service, attr, value)
        service.save()
        return service

    def offer_support(self, service_id, client_id):
        service = self.get(pk=service_id)
        return f"Support offered to client {client_id} for service {service_id}"

class InsuranceQuote(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    coverage_options = models.TextField(blank=True, null=True)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)

    def request_quote(self, provider_id, property_id, coverage_options):
        return self.create(
            provider_id=provider_id,
            property_id=property_id,
            coverage_options=coverage_options,
            premium_amount=0.0,
            valid_until=datetime.date.today() + datetime.timedelta(days=30)
        )

    def update_quote(self, quote_id, coverage_options):
        quote = self.get(pk=quote_id)
        self.coverage_options = coverage_options
        quote.save()
        return quote

    def accept_quote(self, quote_id):
        quote = self.get(pk=quote_id)
        return f"Quote {quote_id} accepted with premium amount {self.premium_amount}"
