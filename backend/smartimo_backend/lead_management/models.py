from django.db import models
from core.models import Communication, TimeStampedModel
from property_listing.models import RealEstateAgent
from sales_management.models import Lead

class LeadCaptureForm(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    form_fields = models.JSONField(blank=True, null=True)
    form_url = models.URLField(blank=True, null=True)
    customization_options = models.JSONField(blank=True, null=True)

    def create_form(self):
        self.save()
        return self

    def customize_form(self, fields, options):
        self.form_fields = fields
        self.customization_options = options
        self.save()

    def publish_form(self):
        return f"Form published at {self.form_url}"
    

class SocialMediaLead(TimeStampedModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    platform = models.CharField(max_length=255, choices=[('facebook', 'Facebook'), ('instagram', 'Instagram'), ('tiktok', 'Tiktok'), ('twitter', 'Twitter')], default='facebook')
    campaign_id = models.CharField(max_length=255, blank=True, null=True)
    ad_creative = models.CharField(max_length=255, blank=True, null=True)
    engagement_metrics = models.JSONField(blank=True, null=True)

    def track_lead(self):
        return f"Tracking lead from {self.platform} campaign {self.campaign_id}"

    def view_engagement_metrics(self):
        return self.engagement_metrics

    def optimize_campaign(self):
        return f"Optimizing campaign with ad creative {self.ad_creative}"


class OfflineLead(TimeStampedModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    source = models.CharField(max_length=255, blank=True, null=True)
    event_details = models.TextField(blank=True, null=True)
    contact_information = models.JSONField(blank=True, null=True)

    def import_lead(self):
        return f"Lead imported from {self.source}"

    def categorize_lead(self, category):
        self.source = category
        self.save()

    def track_engagement(self):
        return f"Tracking engagement for lead {self.lead.user_id}"


class LeadAssignment(TimeStampedModel):
    assignment = models.AutoField(primary_key=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    criteria = models.JSONField(blank=True, null=True)
    assignment_date = models.DateField(blank=True, null=True)

    def assign_lead(self):
        return f"Lead {self.lead.user_id} assigned to agent {self.agent.user_id}"

    def update_assignment(self, new_criteria, new_agent):
        self.criteria = new_criteria
        self.agent_id = new_agent
        self.save()

    def view_assignment_details(self):
        return {
            "lead_id": self.lead.user_id,
            "agent_id": self.agent.user_id,
            "criteria": self.criteria,
            "assignment_date": self.assignment_date
        }


class LeadCommunication(Communication):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    agent_id = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    communication_type = models.CharField(max_length=255, choices=[('sms', 'SMS'), ('email', 'Email'), ('call', 'Call')], default='email')
    status = models.CharField(max_length=255, choices=[('completed', 'Complted'), ('pending', 'Pending')], default='pending')

    def track_interactions(self):
        return f"Tracking interactions with lead {self.lead.user_id}"

    def view_communication_history(self):
        return LeadCommunication.objects.filter(lead=self.lead.user_id).order_by('-created_at')


class LeadNurturing(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    communication_tools = models.JSONField(blank=True, null=True)
    follow_up_actions = models.JSONField(blank=True, null=True)
    engagement_metrics = models.JSONField(blank=True, null=True)

    def schedule_follow_up(self, actions):
        self.follow_up_actions = actions
        self.save()

    def create_drip_campaign(self, campaign_details):
        return f"Drip campaign created with details {campaign_details}"

    def track_engagement(self):
        return self.engagement_metrics
