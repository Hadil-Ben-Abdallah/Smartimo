from django.db import models
from core.models import TimeStampedModel
from lease_rental_management.models import PropertyManager

class TenantPortalBranding(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    logo = models.URLField(max_length=255, null=True, blank=True)
    brand_colors = models.JSONField(null=True, blank=True)
    header_banner = models.URLField(max_length=255, null=True, blank=True)
    background_image = models.URLField(max_length=255, null=True, blank=True)
    font_styles = models.JSONField(null=True, blank=True)

    def upload_logo(self, logo_url):
        self.logo = logo_url
        self.save()

    def set_brand_colors(self, colors):
        self.brand_colors = colors
        self.save()

    def configure_header_banner(self, banner_url):
        self.header_banner = banner_url
        self.save()

    def apply_custom_fonts(self, fonts):
        self.font_styles = fonts
        self.save()

    def preview_branding(self):
        return {
            "logo": self.logo,
            "brand_colors": self.brand_colors,
            "header_banner": self.header_banner,
            "background_image": self.background_image,
            "font_styles": self.font_styles,
        }

class TenantPortalLayout(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    modules = models.JSONField(null=True, blank=True)
    navigation_structure = models.JSONField(null=True, blank=True)

    def customize_layout(self, modules):
        self.modules = modules
        self.save()

    def set_navigation_structure(self, structure):
        self.navigation_structure = structure
        self.save()

    def preview_layout(self):
        return {
            "modules": self.modules,
            "navigation_structure": self.navigation_structure,
        }

    def ensure_responsive_design(self):
        for module in self.modules:
            module['responsive'] = True
        self.save()

class TenantPortalSettings(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    default_communication_channel = models.CharField(max_length=50, null=True, blank=True)
    notification_preferences = models.JSONField(null=True, blank=True)
    language_settings = models.JSONField(null=True, blank=True)

    def configure_communication_channel(self, channel):
        self.default_communication_channel = channel
        self.save()

    def set_notification_preferences(self, preferences):
        self.notification_preferences = preferences
        self.save()

    def customize_language_settings(self, languages):
        self.language_settings = languages
        self.save()

    def preview_settings(self):
        return {
            "default_communication_channel": self.default_communication_channel,
            "notification_preferences": self.notification_preferences,
            "language_settings": self.language_settings,
        }

class CustomPage(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def create_page(self, title, content):
        self.title = title
        self.content = content
        self.save()

    def edit_page(self, new_title=None, new_content=None):
        if new_title:
            self.title = new_title
        if new_content:
            self.content = new_content
        self.save()

    def delete_page(self):
        self.delete()

    def publish_page(self):
        self.save()

    def view_page_statistics(self):
        return {
            "views": 100,
            "engagement": 75,
        }

class TenantEngagementAnalytics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    page_views = models.JSONField(default=dict, null=True, blank=True)
    session_duration = models.FloatField(default=0.0, null=True, blank=True)
    feature_adoption_rates = models.JSONField(default=dict)
    engagement_trends = models.JSONField(default=dict)

    def track_page_views(self, page_id):
        if page_id in self.page_views:
            self.page_views[page_id] += 1
        else:
            self.page_views[page_id] = 1
        self.save()

    def analyze_session_duration(self, duration):
        self.session_duration = (self.session_duration + duration) / 2
        self.save()

    def calculate_feature_adoption(self, feature_id):
        if feature_id in self.feature_adoption_rates:
            self.feature_adoption_rates[feature_id] += 1
        else:
            self.feature_adoption_rates[feature_id] = 1
        self.save()

    def identify_engagement_trends(self, trend_data):
        self.engagement_trends.update(trend_data)
        self.save()

    def generate_engagement_report(self):
        return {
            "page_views": self.page_views,
            "session_duration": self.session_duration,
            "feature_adoption_rates": self.feature_adoption_rates,
            "engagement_trends": self.engagement_trends,
        }

