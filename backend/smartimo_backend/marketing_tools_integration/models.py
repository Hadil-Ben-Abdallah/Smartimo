from django.db import models
from core.models import Property

class MarketingProperty(Property):
    virtual_tours = models.JSONField(null=True, blank=True)
    media_optimization_recommendations = models.TextField(null=True, blank=True)

    def create_listing(self):
        self.save()
        return self

    def upload_media(self, media_type, media_content):
        if media_type == 'photo':
            self.photos.append(media_content)
        elif media_type == 'video':
            self.videos.append(media_content)
        elif media_type == 'virtual_tour':
            self.virtual_tours.append(media_content)
        self.save()

    def edit_media(self, media_type, media_content, index):
        if media_type == 'photo':
            self.photos[index] = media_content
        elif media_type == 'video':
            self.videos[index] = media_content
        elif media_type == 'virtual_tour':
            self.virtual_tours[index] = media_content
        self.save()

    def get_optimization_recommendations(self):
        recommendations = f"Optimize the photos by reducing size and enhancing brightness. " \
                          f"For videos, ensure proper lighting and stable recording. " \
                          f"Virtual tours should be interactive and easy to navigate."
        self.media_optimization_recommendations = recommendations
        self.save()
        return recommendations

class ListingDistribution(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(MarketingProperty, on_delete=models.CASCADE)
    channel = models.CharField(max_length=255)
    target_audience = models.TextField()
    category = models.CharField(max_length=255)
    views = models.IntegerField(default=0)
    inquiries = models.IntegerField(default=0)
    engagement_metrics = models.JSONField(null=True, blank=True)

    def distribute_listing(self):
        self.views += 100  # Simulating the distribution and increase in views
        self.inquiries += 10
        self.engagement_metrics = {"likes": 50, "shares": 20, "comments": 5}
        self.save()
        return f"Listing distributed to {self.channel}. Current views: {self.views}"

    def select_target_audience(self, audience_segments):
        self.target_audience = audience_segments
        self.save()
        return f"Target audience set to: {self.target_audience}"

    def track_performance(self):
        return {
            "views": self.views,
            "inquiries": self.inquiries,
            "engagement_metrics": self.engagement_metrics
        }

class SocialMediaPost(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(MarketingProperty, on_delete=models.CASCADE)
    platform = models.CharField(max_length=255)
    content = models.TextField()
    scheduled_time = models.DateTimeField()
    engagement_metrics = models.JSONField(null=True, blank=True)

    def create_post(self):
        self.save()
        return f"Post created on {self.platform} for property ID {self.property.property_id}"

    def schedule_post(self, scheduled_time):
        self.scheduled_time = scheduled_time
        self.save()
        return f"Post scheduled on {self.platform} for {self.scheduled_time}"

    def track_performance(self):
        return self.engagement_metrics or {"likes": 0, "shares": 0, "comments": 0}

class AdvertisingCampaign(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(MarketingProperty, on_delete=models.CASCADE)
    platform = models.CharField(max_length=255)
    target_audience = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    bidding_strategy = models.CharField(max_length=255)
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    cpa = models.DecimalField(max_digits=10, decimal_places=2)

    def launch_campaign(self):
        self.impressions += 1000
        self.clicks += 100
        self.conversions += 5
        self.cpa = self.budget / self.conversions if self.conversions > 0 else 0
        self.save()
        return f"Campaign launched on {self.platform}. Impressions: {self.impressions}, CPA: {self.cpa}"

    def define_target_audience(self, audience_criteria):
        self.target_audience = audience_criteria
        self.save()
        return f"Target audience defined: {self.target_audience}"

    def track_performance(self):
        return {
            "impressions": self.impressions,
            "clicks": self.clicks,
            "conversions": self.conversions,
            "cpa": self.cpa
        }

class MarketingAnalytics(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(MarketingProperty, on_delete=models.CASCADE)
    campaign = models.ForeignKey(AdvertisingCampaign, on_delete=models.CASCADE)
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    cpl = models.DecimalField(max_digits=10, decimal_places=2)
    roi = models.DecimalField(max_digits=10, decimal_places=2)
    custom_reports = models.JSONField(null=True, blank=True)

    def generate_report(self):
        report = {
            "impressions": self.impressions,
            "clicks": self.clicks,
            "conversions": self.conversions,
            "cpl": self.cpl,
            "roi": self.roi
        }
        self.custom_reports = report
        self.save()
        return report

    def compare_performance(self, other_campaign):
        performance_comparison = {
            "current_campaign": {
                "impressions": self.impressions,
                "clicks": self.clicks,
                "conversions": self.conversions
            },
            "other_campaign": {
                "impressions": other_campaign.impressions,
                "clicks": other_campaign.clicks,
                "conversions": other_campaign.conversions
            }
        }
        return performance_comparison

    def get_insights(self):
        insights = f"Focus on platforms with higher conversions. " \
                f"Consider increasing budget for channels with lower CPA."
        return insights

