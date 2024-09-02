from django.db import models
from task_calendar_management.models import Event
from core.models import User, Resource, TimeStampedModel

class Community(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def create_forum(self, name: str, description: str):
        return Forum.objects.create(community=self, name=name, description=description)

    def post_announcement(self, title: str, content: str, category: str):
        return CommunityAnnouncement.objects.create(community=self, title=title, content=content, category=category)

    def schedule_event(self, name: str, description: str, date, time, location: str):
        return CommunityEvent.objects.create(
            community=self, name=name, description=description, date=date, time=time, location=location
        )

    def add_resource(self, category: str):
        return CommunityResource.objects.create(community=self, category=category)


class Forum(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, related_name='forums', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def create_thread(self, title: str, content: str):
        return Thread.objects.create(forum=self, title=title, content=content)

    def post_reply(self, thread_id: int, content: str):
        thread = Thread.objects.get(thread_id=thread_id)
        return Reply.objects.create(thread=thread, content=content)

    def moderate_post(self, reply_id: int, action: str):
        reply = Reply.objects.get(reply_id=reply_id)
        if action == 'approve':
            reply.status = 'approved'
        elif action == 'flag':
            reply.status = 'flagged'
        elif action == 'ban':
            reply.status = 'banned'
        reply.save()


class Thread(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    forum = models.ForeignKey(Forum, related_name='threads', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)


class Reply(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    thread = models.ForeignKey(Thread, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')


class CommunityAnnouncement(TimeStampedModel):
    community = models.ForeignKey(Community, related_name='announcements', on_delete=models.CASCADE)
    category = models.CharField(max_length=255, choices=[('news', 'News'), ('updates', 'Updates'), ('events', 'Events')], default='news')

    def subscribe(self, user_id: int):
        return Subscriber.objects.create(announcement=self, user_id=user_id)

class Subscriber(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    announcement = models.ForeignKey(CommunityAnnouncement, related_name='subscribers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CommunityEvent(Event):
    community = models.ForeignKey(Community, related_name='events', on_delete=models.CASCADE)

    def manage_attendees(self):
        return RSVP.objects.filter(event=self)


class RSVP(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(CommunityEvent, related_name='rsvps', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CommunityResource(Resource):
    community = models.ForeignKey(Community, related_name='resources', on_delete=models.CASCADE)
    category = models.CharField(max_length=255, choices=[('service_provider', 'Service Provider'), ('local_business', 'Local Business')], default='service_provider')

    def search(self, criteria: dict):
        return CommunityResource.objects.filter(**criteria)

    def submit_review(self, review_details: str):
        return Review.objects.create(resource=self, details=review_details)

    def update_details(self, details: dict):
        for attr, value in details.items():
            setattr(self, attr, value)
        self.save()


class Review(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(CommunityResource, related_name='reviews', on_delete=models.CASCADE)
    details = models.TextField(blank=True, null=True)


class Poll(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, related_name='polls', on_delete=models.CASCADE)
    question = models.CharField(max_length=255, blank=True, null=True)
    options = models.JSONField(blank=True, null=True)

    def create_poll(self, question: str, options: list):
        self.question = question
        self.options = options
        self.save()

    def vote(self, option_id: int, user_id: int):
        PollVote.objects.create(poll=self, option=option_id, user=user_id)

    def analyze_results(self) -> dict:
        votes = PollVote.objects.filter(poll=self)
        results = {option: votes.filter(option=option).count() for option in self.options}
        return results


class PollVote(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)
    option = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)