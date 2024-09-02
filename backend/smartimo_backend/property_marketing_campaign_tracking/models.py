from django.db import models
from property_marketing_campaigns.models import MarketingCampaign
from sales_management.models import Lead
from core.models import TimeStampedModel

class MarketingCampaignTrack(MarketingCampaign):
    message = models.TextField(blank=True, null=True)
    creative_assets = models.JSONField(blank=True, null=True)

    def delete_campaign(self):
        self.delete()

class WebsiteTraffic(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(MarketingCampaignTrack, on_delete=models.CASCADE)
    page_views = models.IntegerField(blank=True, null=True)
    bounce_rate = models.FloatField(blank=True, null=True)
    session_duration = models.FloatField(blank=True, null=True)
    traffic_source = models.CharField(max_length=255, blank=True, null=True)

    def record_traffic(self, page_views, bounce_rate, session_duration, traffic_source):
        self.page_views = page_views
        self.bounce_rate = bounce_rate
        self.session_duration = session_duration
        self.traffic_source = traffic_source
        self.save()

    def get_traffic_metrics(self):
        return {
            "page_views": self.page_views,
            "bounce_rate": self.bounce_rate,
            "session_duration": self.session_duration,
            "traffic_source": self.traffic_source,
        }

    def analyze_traffic(self):
        effectiveness_score = self.page_views / (self.bounce_rate + 1) * self.session_duration
        return {
            "effectiveness_score": effectiveness_score,
            "traffic_source": self.traffic_source,
        }

class PropertyMarketingLead(Lead):
    campaign = models.ForeignKey(MarketingCampaignTrack, on_delete=models.CASCADE)
    inquiry_date = models.DateField(auto_now_add=True, blank=True, null=True)

    def capture_lead(self, username, email, phone, contact_details, inquiry_date, lead_source, lead_status, property_type):
        self.username = username
        self. email = email
        self.phone = phone
        self.contact_details = contact_details
        self.inquiry_date = inquiry_date
        self.lead_status = lead_status
        self.lead_source = lead_source
        self.property_type = property_type
        self.save()

    def track_lead_progress(self):
        lead_status = "new"
        return {
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "lead_status": lead_status,
            "inquiry_date": self.inquiry_date,
            "contact_details": self.contact_details,
            "lead_source": self.lead_source,
        }

class CampaignPerformanceTrack(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(MarketingCampaignTrack, on_delete=models.CASCADE)
    leads_generated = models.IntegerField(blank=True, null=True)
    conversions = models.IntegerField(blank=True, null=True)
    cost_per_acquisition = models.FloatField(blank=True, null=True)
    roi = models.FloatField(blank=True, null=True)

    def record_performance(self, leads_generated, conversions, cost_per_acquisition, roi):
        self.leads_generated = leads_generated
        self.conversions = conversions
        self.cost_per_acquisition = cost_per_acquisition
        self.roi = roi
        self.save()

    def generate_performance_report(self):
        return {
            "leads_generated": self.leads_generated,
            "conversions": self.conversions,
            "cost_per_acquisition": self.cost_per_acquisition,
            "roi": self.roi,
        }

    def compare_campaigns(self, other_campaign):
        return {
            "current_campaign": self.generate_performance_report(),
            "other_campaign": other_campaign.generate_performance_report(),
        }

class TrackingPixel(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(MarketingCampaignTrack, on_delete=models.CASCADE)
    pixel_code = models.TextField(blank=True, null=True)
    integration_date = models.DateField(blank=True, null=True)

    def add_tracking_pixel(self, pixel_code):
        self.pixel_code = pixel_code
        self.integration_date = models.DateField(auto_now_add=True)
        self.save()

    def remove_tracking_pixel(self):
        self.delete()

    def get_pixel_code(self):
        return self.pixel_code

class CampaignAnalysis(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(MarketingCampaignTrack, on_delete=models.CASCADE)
    channel_performance = models.JSONField(blank=True, null=True)
    audience_segment_performance = models.JSONField(blank=True, null=True)
    property_type_performance = models.JSONField(blank=True, null=True)

    def analyze_by_channel(self):
        best_channel = max(self.channel_performance, key=self.channel_performance.get)
        return {
            "best_channel": best_channel,
            "performance_metrics": self.channel_performance[best_channel],
        }

    def analyze_by_segment(self):
        best_segment = max(self.audience_segment_performance, key=self.audience_segment_performance.get)
        return {
            "best_segment": best_segment,
            "performance_metrics": self.audience_segment_performance[best_segment],
        }

    def analyze_by_property_type(self):
        best_property_type = max(self.property_type_performance, key=self.property_type_performance.get)
        return {
            "best_property_type": best_property_type,
            "performance_metrics": self.property_type_performance[best_property_type],
        }

    def optimize_campaign(self):
        recommendations = {
            "channel_optimization": "Focus on best-performing channels.",
            "audience_optimization": "Target best-performing audience segments.",
            "property_type_optimization": "Invest in marketing for best-performing property types.",
        }
        return recommendations

