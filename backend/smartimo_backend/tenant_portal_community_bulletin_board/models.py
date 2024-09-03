from django.db import models
from core.models import Notification, User, TimeStampedModel
from django.utils import timezone
from lease_rental_management.models import Tenant

class Announcement(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    post_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False, blank=True, null=True)

    def publish(self):
        self.post_date = timezone.now()
        self.is_archived = False
        self.save()

    def archive(self):
        self.is_archived = True
        self.save()

    def remove(self):
        self.delete()

    def update_content(self, title, description, expiration_date):
        self.title = title
        self.description = description
        self.expiration_date = expiration_date
        self.save()

    def get_announcement_info(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "post_date": self.post_date,
            "expiration_date": self.expiration_date,
            "posted_by": self.posted_by.username,
            "is_archived": self.is_archived,
        }

class AnnouncementNotification(Notification):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)

    def get_notification_details(self):
        return {
            "user": self.tenant.user_id,
            "announcement": self.announcement.get_announcement_info(),
            "message": self.message,
            "status": self.status,
            "date": self.date
        }

class Reaction(TimeStampedModel):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('care', 'Care'),
    ]
    id = models.AutoField(primary_key=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES, default='like')

    def add_reaction(self, reaction_type):
        self.reaction_type = reaction_type
        self.save()

    def remove_reaction(self):
        self.delete()

    def get_reactions_summary(self):
        reactions = Reaction.objects.filter(announcement=self.announcement)
        summary = {choice[0]: 0 for choice in self.REACTION_CHOICES}
        for reaction in reactions:
            summary[reaction.reaction_type] += 1
        return summary

class Comment(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    comment_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def add_comment(self, content):
        self.content = content
        self.comment_date = timezone.now()
        self.save()

    def edit_comment(self, content):
        self.content = content
        self.comment_date = timezone.now()
        self.save()

    def delete_comment(self):
        self.delete()

    def get_comment_details(self):
        return {
            "id": self.id,
            "announcement": self.announcement.get_announcement_info(),
            "tenant": self.tenant.username,
            "content": self.content,
            "comment_date": self.comment_date,
        }
