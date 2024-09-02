from django.db import models
from core.models import Property, TimeStampedModel
from lease_rental_management.models import Tenant

class LeaseAgreementGenerator(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lease_start_date = models.DateField(blank=True, null=True)
    lease_end_date = models.DateField(blank=True, null=True)
    rental_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pet_policy = models.TextField(null=True, blank=True)
    amenities = models.JSONField(default=dict, blank=True, null=True)
    custom_clauses = models.JSONField(default=dict, blank=True, null=True)
    legal_template_version = models.CharField(max_length=50, blank=True, null=True)

    def generate_lease_agreement(self):
        lease_content = f"""
        LEASE AGREEMENT
        Property: {self.property.address}
        Tenant: {self.tenant.username}
        Lease Start Date: {self.lease_start_date}
        Lease End Date: {self.lease_end_date}
        Rental Amount: ${self.rental_amount}
        Security Deposit: ${self.security_deposit}
        Pet Policy: {self.pet_policy or 'None'}
        Amenities: {', '.join(self.amenities.get('amenities_list', []))}

        Additional Clauses:
        {self.custom_clauses.get('additional_clauses', 'None')}

        Legal Template Version: {self.legal_template_version}
        """

        return lease_content

    def update_lease_agreement(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()

    def delete_lease_agreement(self):
        self.delete()

    def get_lease_agreement(self):
        return {
            "id": self.id,
            "property": self.property.property_id,
            "tenant": self.tenant.user_id,
            "lease_start_date": self.lease_start_date,
            "lease_end_date": self.lease_end_date,
            "rental_amount": self.rental_amount,
            "security_deposit": self.security_deposit,
            "pet_policy": self.pet_policy,
            "amenities": self.amenities,
            "custom_clauses": self.custom_clauses,
            "legal_template_version": self.legal_template_version,
        }

class LeaseAgreementTemplate(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=100, blank=True, null=True)
    template_content = models.JSONField(default=dict, blank=True, null=True)
    legal_requirements = models.JSONField(default=dict, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)

    def create_template(self, template_name, template_content, legal_requirements):
        self.template_name = template_name
        self.template_content = template_content
        self.legal_requirements = legal_requirements
        self.save()
        return self

    def update_template(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()

    def delete_template(self):
        self.delete()

    def get_template(self):
        return {
            "template_name": self.template_name,
            "template_content": self.template_content,
            "legal_requirements": self.legal_requirements,
            "version": self.version
        }

class MultiPartyAgreement(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    lease_agreement = models.ForeignKey(LeaseAgreementGenerator, on_delete=models.CASCADE)
    party_roles = models.JSONField(default=dict, blank=True, null=True)
    custom_provisions = models.JSONField(default=dict, blank=True, null=True)

    def create_multi_party_agreement(self, lease_agreement, party_roles, custom_provisions):
        self.lease_agreement = lease_agreement
        self.party_roles = party_roles
        self.custom_provisions = custom_provisions
        self.save()
        return self

    def update_multi_party_agreement(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()

    def delete_multi_party_agreement(self):
        self.delete()

    def get_multi_party_agreement(self):
        return {
            "lease_agreement": self.lease_agreement.get_lease_agreement(),
            "party_roles": self.party_roles,
            "custom_provisions": self.custom_provisions
        }

class BrandingOptions(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    generator = models.ForeignKey(LeaseAgreementGenerator, on_delete=models.CASCADE)
    logo_url = models.URLField(blank=True, null=True)
    header_style = models.JSONField(default=dict, blank=True, null=True)
    footer_style = models.JSONField(default=dict, blank=True, null=True)
    font_style = models.CharField(max_length=50, blank=True, null=True)
    color_scheme = models.JSONField(default=dict, blank=True, null=True)

    def apply_branding(self, lease_content):
        header = f"{self.header_style.get('text', '')}\n"
        footer = f"\n{self.footer_style.get('text', '')}"
        branded_content = f"{header}{lease_content}{footer}"
        return branded_content

    def update_branding(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()

    def delete_branding(self):
        self.delete()

    def get_branding(self):
        return {
            "logo_url": self.logo_url,
            "header_style": self.header_style,
            "footer_style": self.footer_style,
            "font_style": self.font_style,
            "color_scheme": self.color_scheme
        }

