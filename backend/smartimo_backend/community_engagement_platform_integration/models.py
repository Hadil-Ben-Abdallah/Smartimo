from django.db import models
from django.contrib.auth.models import User
from core.models import Property, Resource, TimeStampedModel
from lease_rental_management.models import Tenant
from task_calendar_management.models import Event

class CommunityHub(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def create_hub(self, name, description):
        return CommunityHub.objects.create(name=name, description=description)

    def update_hub(self, name=None, description=None):
        if name:
            self.name = name
        if description:
            self.description = description
        self.save()
        return self

    def delete_hub(self):
        self.delete()

    def get_hub_details(self):
        return {
            "id": self.id,
            "property_id": self.property.property_id,
            "name": self.name,
            "description": self.description,
        }

    @staticmethod
    def list_hubs():
        return CommunityHub.objects.all()

class TenantProfile(Tenant):
    photo = models.ImageField(upload_to='tenant_photos/', null=True, blank=True)

    def create_profile(self, user, photo=None):
        return TenantProfile.objects.create(user=user, photo=photo)

    def update_profile(self, photo=None):
        if photo:
            self.photo = photo
        self.save()
        return self

    def delete_profile(self):
        self.delete()

    def get_profile_details(self):
        return {
            "firs_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "cin": self.cin,
            "birth_date": self.birth_date,
            "address": self.address,
            "phone": self.phone,

            "photo": self.photo.url if self.photo else None,
        }

    @staticmethod
    def list_profiles():
        return TenantProfile.objects.all()

class CommunityGroup(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    hub = models.ForeignKey(CommunityHub, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def create_group(self, name, description):
        return CommunityGroup.objects.create(name=name, description=description, hub=self.hub)

    def update_group(self, name=None, description=None):
        if name:
            self.name = name
        if description:
            self.description = description
        self.save()
        return self

    def delete_group(self):
        self.delete()

    def get_group_details(self):
        return {
            "id": self.id,
            "hub_id": self.hub.id,
            "name": self.name,
            "description": self.description,
        }

    @staticmethod
    def list_groups():
        return CommunityGroup.objects.all()

    def join_group(self, tenant_profile):
        pass

    def leave_group(self, tenant_profile):
        pass

class CommunityEngagementEvent(Event):
    hub = models.ForeignKey(CommunityHub, on_delete=models.CASCADE)

    def create_event(self, name, topic, date):
        return CommunityEngagementEvent.objects.create(
            hub=self.hub,
            name=name,
            description=topic,
            date=date
        )

    def update_event(self, name=None, topic=None, date=None):
        if name:
            self.name = name
        if topic:
            self.topic = topic
        if date:
            self.date = date
        self.save()
        return self

    def delete_event(self):
        self.delete()

    def get_event_details(self):
        return {
            "hub_id": self.hub.id,
            "name": self.name,
            "description": self.topic,
            "date": self.date,
        }

    @staticmethod
    def list_events():
        return CommunityEngagementEvent.objects.all()

class CommunityEngagementDiscussion(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(CommunityGroup, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(TenantProfile, on_delete=models.CASCADE)

    def create_discussion(self, title, content, author):
        return CommunityEngagementDiscussion.objects.create(
            group=self.group,
            title=title,
            content=content,
            author=author
        )

    def update_discussion(self, title=None, content=None):
        if title:
            self.title = title
        if content:
            self.content = content
        self.save()
        return self

    def delete_discussion(self):
        self.delete()

    def get_discussion_details(self):
        return {
            "id": self.id,
            "group_id": self.group.id,
            "title": self.title,
            "content": self.content,
            "author_id": self.author.user_id,
        }

    @staticmethod
    def list_discussions():
        return CommunityEngagementDiscussion.objects.all()

    def post_comment(self, content, author):
        pass

    def moderate_discussion(self, content=None, action=None):
        pass

class CommunityEngagementResource(Resource):
    hub = models.ForeignKey(CommunityHub, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, blank=True, null=True)
    operating_hours = models.CharField(max_length=255, blank=True, null=True)

    def add_resource(self, title, type, description, contact_info, operating_hours):
        return CommunityEngagementResource.objects.create(
            hub=self.hub,
            title=title,
            type=type,
            description=description,
            operating_hours=operating_hours,
            contact_info=contact_info
        )

    def update_resource(self, type=None, description=None, contact_info=None, operating_hours=None, title=None):
        if title:
            self.title = title
        if type:
            self.type = type
        if description:
            self.description = description
        if contact_info:
            self.contact_info = contact_info
        if operating_hours:
            self.operating_hours = operating_hours
        self.save()
        return self

    def delete_resource(self):
        self.delete()

    def get_resource_details(self):
        return {
            "hub_id": self.hub.id,
            "title": self.title,
            "type": self.type,
            "description": self.description,
            "contact_info": self.contact_info,
            "operating_hours": self.operating_hours,
        }

    @staticmethod
    def list_resources():
        return CommunityEngagementResource.objects.all()

class EngagementReward(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    points = models.IntegerField(blank=True, null=True)
    badge = models.CharField(max_length=255, blank=True, null=True)

    def track_engagement(self, tenant, points):
        reward = EngagementReward.objects.get_or_create(tenant=tenant)
        reward.points += points
        reward.save()
        return reward

    def award_points(self, tenant, points):
        reward = EngagementReward.objects.get_or_create(tenant=tenant)
        reward.points += points
        reward.save()
        return reward

    def assign_badge(self, tenant, badge):
        reward = EngagementReward.objects.get_or_create(tenant=tenant)
        reward.badge = badge
        reward.save()
        return reward

    def get_rewards(self):
        return {
            "tenant_id": self.tenant.user_id,
            "points": self.points,
            "badge": self.badge,
        }

    @staticmethod
    def list_rewards():
        return EngagementReward.objects.all()

    @staticmethod
    def display_leaderboard():
        return EngagementReward.objects.order_by('-points')

