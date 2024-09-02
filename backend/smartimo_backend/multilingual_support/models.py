from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import Property, User, TimeStampedModel
from property_listing.models import RealEstateAgent
from lease_rental_management.models import Tenant

class MultilingualContent(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French')], default='en')
    content_type = models.CharField(max_length=50, choices=[('property_description', 'Property Description'), ('lease_agreement', 'Lease Agreement'), ('communication_template', 'Communication Template')], default='lease_agreement')
    original_content = models.TextField(blank=True, null=True)
    translated_content = models.TextField(blank=True, null=True)
    translation_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def create_content(self, property_id, language, content_type, original_content):
        self.property = property_id
        self.language = language
        self.content_type = content_type
        self.original_content = original_content
        self.save()

    def update_content(self, content_id, new_content):
        content = MultilingualContent.objects.get(id=content_id)
        content.original_content = new_content
        content.save()

    def translate_content(self, content_id, target_language):
        content = MultilingualContent.objects.get(id=content_id)
        content.translated_content = f"Translated to {target_language}: {content.original_content}"
        content.translation_status = 'completed'
        content.save()

    def get_content(self, content_id):
        return MultilingualContent.objects.get(id=content_id)


class MultilingualTenantPortal(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=10, choices=[('en', _('English')), ('es', _('Spanish')), ('fr', _('French'))], default='en')
    lease_agreements = models.TextField(blank=True, null=True)
    rental_policies = models.TextField(blank=True, null=True)
    property_info = models.TextField(blank=True, null=True)

    def set_language_preference(self, tenant_id, language):
        portal = MultilingualTenantPortal.objects.get(tenant_id=tenant_id)
        portal.preferred_language = language
        portal.save()

    def get_lease_agreements(self, tenant_id):
        portal = MultilingualTenantPortal.objects.get(tenant_id=tenant_id)
        return portal.lease_agreements

    def get_rental_policies(self, tenant_id):
        portal = MultilingualTenantPortal.objects.get(tenant_id=tenant_id)
        return portal.rental_policies

    def get_property_info(self, tenant_id):
        portal = MultilingualTenantPortal.objects.get(tenant_id=tenant_id)
        return portal.property_info


class MultilingualMarketing(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French')], default='en')
    marketing_material = models.TextField(blank=True, null=True)
    approval_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved')], default='pending')

    def create_marketing_material(self, agent_id, property_id, language, content):
        self.agent = agent_id
        self.property = property_id
        self.language = language
        self.marketing_material = content
        self.save()

    def update_marketing_material(self, marketing_id, new_content):
        material = MultilingualMarketing.objects.get(marketing_id=marketing_id)
        material.marketing_material = new_content
        material.save()

    def approve_marketing_material(self, marketing_id):
        material = MultilingualMarketing.objects.get(marketing_id=marketing_id)
        material.approval_status = 'approved'
        material.save()

    def get_marketing_material(self, marketing_id):
        return MultilingualMarketing.objects.get(marketing_id=marketing_id)


class InvestorRelations(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    preferred_language = models.CharField(max_length=10, choices=[('en', 'English'), ('es', 'Spanish'), ('fr','French')], default='en')
    project_updates = models.TextField(blank=True, null=True)
    financial_reports = models.TextField(blank=True, null=True)
    performance_metrics = models.TextField(blank=True, null=True)
    investment_documents = models.TextField(blank=True, null=True)

    def set_language_preference(self, investor_id, language):
        investor = InvestorRelations.objects.get(id=investor_id)
        investor.preferred_language = language
        investor.save()

    def get_project_updates(self, investor_id):
        investor = InvestorRelations.objects.get(id=investor_id)
        return investor.project_updates

    def get_financial_reports(self, investor_id):
        investor = InvestorRelations.objects.get(id=investor_id)
        return investor.financial_reports

    def get_performance_metrics(self, investor_id):
        investor = InvestorRelations.objects.get(id=investor_id)
        return investor.performance_metrics

    def get_investment_documents(self, investor_id):
        return InvestorRelations.objects.get(id=investor_id).investment_documents


class MultilingualSupport(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=10, choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French')], default='en')
    faq_articles = models.TextField(blank=True, null=True)
    help_docs = models.TextField(blank=True, null=True)
    support_channels = models.TextField(blank=True, null=True)

    def set_language_preference(self, user_id, language):
        support = MultilingualSupport.objects.get(user_id=user_id)
        support.preferred_language = language
        support.save()

    def get_faq_articles(self, user_id):
        support = MultilingualSupport.objects.get(user_id=user_id)
        return support.faq_articles

    def get_help_docs(self, user_id):
        support = MultilingualSupport.objects.get(user_id=user_id)
        return support.help_docs

    def get_support_channels(self, user_id):
        support = MultilingualSupport.objects.get(user_id=user_id)
        return support.support_channels

    def translate_support_content(self, content_id, target_language):
        support = MultilingualSupport.objects.get(support_id=content_id)
        translated_content = f"Translated to {target_language}: {support.faq_articles}"
        return translated_content

