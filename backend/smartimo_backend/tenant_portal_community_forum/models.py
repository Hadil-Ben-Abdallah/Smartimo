from django.db import models
from community_management_features.models import Community, Announcement
from lease_rental_management.models import Tenant, PropertyManager
from core.models import Category

class ForumTopic(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    tags = models.CharField(max_length=255, blank=True, null=True)

    def create_topic(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author
        self.save()

    def reply_to_topic(self, content, author):
        reply = ForumReply.objects.create(topic=self, content=content, author=author)
        reply.save()

    def tag_topic(self, tags):
        self.tags = tags
        self.save()

    def like_topic(self):
        print(f"Topic '{self.title}' liked by a user.")

class ForumCategory(Category):
    topic = models.ManyToManyField(ForumTopic, on_delete=models.CASCADE)

    def create_category(self, name, description, topic_id):
        self.name = name
        self.description = description
        self.topic.id = topic_id
        self.save()

    def add_topic(self, topic):
        if not hasattr(self, 'topic'):
            self.topic = []
        self.topic.append(topic)
        self.save()

    def remove_topic(self, topic_id):
        if hasattr(self, 'topic'):
            self.topic = [topic for topic in self.topic if topic != topic_id]
            self.save()


class CommunityForum(Community):
    categories = models.ManyToManyField(ForumCategory, related_name='forums')
    moderators = models.ManyToManyField(PropertyManager, related_name='forums')

    def assign_moderator(self, property_manager):
        self.moderators.add(property_manager)
        self.save()

    def add_category(self, category):
        self.categories.add(category)
        self.save()

    def remove_category(self, category):
        self.categories.remove(category)
        self.save()

    def enforce_guidelines(self):
        pass


class ForumReply(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    quoted_reply = models.TextField(blank=True, null=True)
    likes = models.IntegerField(default=0, blank=True, null=True)

    def create_reply(self, topic, content, author, quoted_reply=None):
        self.topic = topic
        self.content = content
        self.author = author
        self.quoted_reply = quoted_reply
        self.save()

    def like_reply(self):
        self.likes += 1
        self.save()

    def mention_user(self, tenant):
        print(f"{self.author.username} mentioned {Tenant.username} in a reply.")


class ForumModeration(models.Model):
    id = models.AutoField(primary_key=True)
    forum = models.ForeignKey(CommunityForum, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=255, choices=[('content', 'Content'), ('report', 'Report'), ('removal', 'Removal'), ('user_ban', 'User ban')], default='content')
    target = models.IntegerField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)

    def moderate_content(self, action_type, target_id, reason):
        self.action_type = action_type
        self.target = target_id
        self.reason = reason
        self.save()

        if action_type == "ban_user":
            Tenant.objects.filter(id=target_id).update(is_banned=True)
        elif action_type == "removal'":
            ForumTopic.objects.filter(id=target_id).delete()

    def report_content(self, target_id, reason):
        moderation_action = ForumModeration.objects.create(
            forum=self.forum, action_type="report", target_id=target_id, reason=reason)
        print(f"Content reported: {moderation_action.reason}")

    def review_reports(self):
        reports = ForumModeration.objects.filter(action_type="report")
        for report in reports:
            print(f"Reviewing report: {report.reason}")


class ForumAnnouncement(models.Model):
    forum = models.ForeignKey(CommunityForum, on_delete=models.CASCADE)

    def create_announcement(self, title, description, post_date, expiration_date, is_archived, posted_by):
        self.title = title
        self.description = description
        self.post_date = post_date
        self.expiration_date =expiration_date
        self.is_archived = is_archived
        self.category = is_archived
        self.posted_by = posted_by
        self.save()

    def schedule_announcement(self, scheduled_time):
        print(f"Announcement '{self.title}' scheduled for {scheduled_time}")

    def notify_tenants(self):
        tenants = Tenant.objects.all()
        for tenant in tenants:
            print(f"Notification sent to {tenant.username}: {self.title}")

