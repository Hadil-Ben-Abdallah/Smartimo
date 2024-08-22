from django.db import models
from django.utils import timezone
from core.models import Resource
from property_listing.models import Agency, RealEstateAgent

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    resources = models.JSONField(blank=True, null=True)

    def create_author(self, name, bio):
        return self.create(name=name, bio=bio)

    def update_author(self, author_id, details):
        author = self.get(id=author_id)
        for attr, value in details.items():
            setattr(author, attr, value)
        author.save()
        return author

    def add_resource(self, author_id, resource_id):
        author = self.get(id=author_id)
        resource = EducationalResource.objects.get(id=resource_id)
        self.resources.add(resource)
        return author

class Trainer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    sessions = models.JSONField(blank=True, null=True)

    def create_trainer(self, name, bio):
        return self.create(name=name, bio=bio)

    def update_trainer(self, trainer_id, details):
        trainer = self.get(id=trainer_id)
        for attr, value in details.items():
            setattr(trainer, attr, value)
        trainer.save()
        return trainer

    def schedule_session(self, trainer_id, session_id):
        trainer = self.get(id=trainer_id)
        session = LiveTrainingSession.objects.get(id=session_id)
        self.sessions.add(session)
        return trainer

class EducationProvider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_info = models.TextField(blank=True, null=True)
    courses = models.JSONField(blank=True, null=True)

    def register_provider(self, name, contact_info):
        return self.create(name=name, contact_info=contact_info)

    def update_provider(self, provider_id, details):
        provider = self.get(id=provider_id)
        for attr, value in details.items():
            setattr(provider, attr, value)
        provider.save()
        return provider

    def offer_course(self, provider_id, course_id):
        provider = self.get(id=provider_id)
        course = CertificationCourse.objects.get(id=course_id)
        self.courses.add(course)
        return provider

class EducationalResource(Resource):
    category = models.CharField(max_length=255, blank=True, null=True)
    format = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content_url = models.URLField(blank=True, null=True)

    def add_resource(self, title, description, category, format, content_url, author_id):
        author = Author.objects.get(id=author_id)
        return self.create(
            title=title,
            description=description,
            category=category,
            format=format,
            content_url=content_url,
            author=author
        )

    def update_resource(self, resource_id, details):
        resource = self.get(id=resource_id)
        for attr, value in details.items():
            setattr(resource, attr, value)
        resource.save()
        return resource

    def filter_resources(self, category, format):
        return self.filter(category=category, format=format)
    

class LiveTrainingSession(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    event_url = models.URLField(blank=True, null=True)
    max_participants = models.PositiveIntegerField(blank=True, null=True)

    def schedule_session(self, title, description, date_time, trainer_id, event_url, max_participants):
        trainer = Trainer.objects.get(id=trainer_id)
        return self.create(
            title=title,
            description=description,
            date_time=date_time,
            trainer=trainer,
            event_url=event_url,
            max_participants=max_participants
        )

    def update_session(self, session_id, details):
        session = self.get(id=session_id)
        for attr, value in details.items():
            setattr(session, attr, value)
        session.save()
        return session

    def register_for_session(self, agent_id, session_id):
        pass

    def send_reminders(self, session_id):
        pass

    def host_interactive_features(self, session_id):
        pass

class CertificationCourse(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    provider = models.ForeignKey(EducationProvider, on_delete=models.CASCADE)
    credits = models.PositiveIntegerField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    enrollment_url = models.URLField(blank=True, null=True)

    def create_course(self, title, description, provider_id, credits, duration, enrollment_url):
        provider = EducationProvider.objects.get(id=provider_id)
        return self.create(
            title=title,
            description=description,
            provider=provider,
            credits=credits,
            duration=duration,
            enrollment_url=enrollment_url
        )

    def update_course(self, course_id, details):
        course = self.get(id=course_id)
        for attr, value in details.items():
            setattr(course, attr, value)
        course.save()
        return course

    def enroll_in_course(self, agent_id, course_id):
        pass

    def track_progress(self, agent_id, course_id):
        pass

    def verify_certification(self, agent_id, course_id):
        pass


class TrainingAgent(RealEstateAgent):
    certifications = models.ManyToManyField(CertificationCourse, related_name='certified_agents', blank=True)

    def create_agent(self, name, email, profile):
        return self.create(name=name, email=email, profile=profile)

    def update_agent(self, agent_id, details):
        agent = self.get(id=agent_id)
        for attr, value in details.items():
            setattr(agent, attr, value)
        agent.save()
        return agent

    def track_learning_progress(self, agent_id):
        pass

    def showcase_certifications(self, agent_id):
        agent = self.get(id=agent_id)
        return self.certifications.all()


class TrainingProgram(models.Model):
    id = models.AutoField(primary_key=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    modules = models.JSONField(blank=True, null=True)
    mentors = models.ManyToManyField(TrainingAgent, related_name='training_programs', blank=True)

    def create_program(self, agency_id, title, description, modules, mentors):
        agency = Agency.objects.get(id=agency_id)
        mentors = TrainingAgent.objects.filter(id__in=mentors)
        return self.create(
            agency=agency_id,
            title=title,
            description=description,
            modules=modules,
            mentors=mentors
        )

    def update_program(self, program_id, details):
        program = self.get(id=program_id)
        for attr, value in details.items():
            setattr(program, attr, value)
        program.save()
        return program

    def assign_mentor(self, program_id, mentor_id):
        program = self.get(id=program_id)
        mentor = TrainingAgent.objects.get(id=mentor_id)
        program.mentors.add(mentor)
        return program


    def provide_feedback(self, agent_id, program_id, feedback):
        pass


class CommunityDiscussion(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(TrainingAgent, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)
    participants = models.JSONField()
    posts = models.JSONField()

    def start_discussion(self, topic, description, created_by_id):
        creator = TrainingAgent.objects.get(id=created_by_id)
        return self.create(
            topic=topic,
            description=description,
            created_by=creator
        )

    def update_discussion(self, discussion_id, details):
        discussion = self.get(id=discussion_id)
        for attr, value in details.items():
            setattr(discussion, attr, value)
        discussion.save()
        return discussion

    def add_participant(self, discussion_id, agent_id):
        discussion = self.get(id=discussion_id)
        agent = TrainingAgent.objects.get(id=agent_id)
        self.participants.add(agent)
        return discussion

