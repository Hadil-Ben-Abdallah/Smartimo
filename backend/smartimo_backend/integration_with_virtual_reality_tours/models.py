from django.db import models
from django.utils import timezone
from core.models import Property, User, TimeStampedModel
from property_listing.models import RealEstateAgent


class VRTour(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    vr_content = models.URLField(blank=True, null=True)
    tour_type = models.CharField(max_length=50, choices=[('360-degree_photo', '360-degree Photo'), ('video_walkthrough', 'Video Walkthrough')], default='360-degree_photo')
    upload_date = models.DateTimeField(default=timezone.now)
    viewing_settings = models.JSONField(blank=True, null=True)

    def upload_vr_tour(self, vr_content, tour_type, viewing_settings):
        self.vr_content = vr_content
        self.tour_type = tour_type
        self.viewing_settings = viewing_settings
        self.save()

    def edit_vr_tour(self, vr_content=None, tour_type=None, viewing_settings=None):
        if vr_content:
            self.vr_content = vr_content
        if tour_type:
            self.tour_type = tour_type
        if viewing_settings:
            self.viewing_settings = viewing_settings
        self.save()

    def get_vr_tour(self):
        return {
            "id": self.id,
            "property": self.property.property_id,
            "vr_content": self.vr_content,
            "tour_type": self.tour_type,
            "upload_date": self.upload_date,
            "viewing_settings": self.viewing_settings,
        }

class VRTourAccess(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(VRTour, on_delete=models.CASCADE)
    access_date = models.DateTimeField(default=timezone.now)
    interaction_data = models.JSONField(blank=True, null=True)

    def track_access(self, user_id, interaction_data):
        self.user.user_id = user_id
        self.interaction_data = interaction_data
        self.save()

    def generate_access_report(self):
        return {
            "id": self.id,
            "tour": self.tour.id,
            "user": self.user.user_id,
            "access_date": self.access_date,
            "interaction_data": self.interaction_data,
        }

class VRPresentation(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    tour = models.ForeignKey(VRTour, on_delete=models.CASCADE)
    presentation_date = models.DateTimeField(default=timezone.now)
    session = models.CharField(max_length=100, blank=True, null=True)
    presentation_notes = models.TextField(blank=True, null=True)

    def initiate_presentation(self, agent_id, tour_id, session):
        self.agent.user_id = agent_id
        self.tour = VRTour.objects.get(id=tour_id)
        self.session = session
        self.save()

    def share_vr_tour(self):
        return {
            "agent": self.agent.user_id,
            "presentation_date": self.presentation_date,
            "session": self.session,
            "presentation_notes": self.presentation_notes,
        }

    def add_notes(self, notes):
        self.presentation_notes = notes
        self.save()

class VRTourAnalytics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tour = models.ForeignKey(VRTour, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0, blank=True, null=True)
    interaction_duration = models.DurationField(default=timezone.timedelta())
    popular_segments = models.JSONField(blank=True, null=True)
    user_demographics = models.JSONField(blank=True, null=True)

    def generate_analytics_report(self):
        return {
            "tour": self.tour.id,
            "views": self.views,
            "interaction_duration": str(self.interaction_duration),
            "popular_segments": self.popular_segments,
            "user_demographics": self.user_demographics,
        }

    def analyze_engagement(self):
        return {
            "views": self.views,
            "interaction_duration": str(self.interaction_duration),
            "popular_segments": self.popular_segments,
        }

class AdvancedVRFeature(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    feature_name = models.CharField(max_length=100, choices=[('spatial_audio', 'Spatial Audio'), ('interactive_hotspots', 'Interactive Hotspots'), ('annotations', 'Annotations'), ('3D_modeling', '3D Modeling')], default='spatial_audio')
    feature_description = models.TextField(blank=True, null=True)
    integration_status = models.CharField(max_length=50, blank=True, null=True)

    def integrate_feature(self, feature_name, feature_description):
        self.feature_name = feature_name
        self.feature_description = feature_description
        self.integration_status = 'Integrated'
        self.save()

    def update_feature(self, feature_name=None, feature_description=None, integration_status=None):
        if feature_name:
            self.feature_name = feature_name
        if feature_description:
            self.feature_description = feature_description
        if integration_status:
            self.integration_status = integration_status
        self.save()

    def get_feature_details(self):
        return {
            "id": self.id,
            "feature_name": self.feature_name,
            "feature_description": self.feature_description,
            "integration_status": self.integration_status,
        }

