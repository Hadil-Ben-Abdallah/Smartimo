from django.db import models
from core.models import SalesOpportunity, Property, TimeStampedModel 
from property_listing.models import RealEstateAgent
from client_management.models import Client, Interaction

class Lead(Client):
    lead_source = models.CharField(max_length=50, choices=[('facebook', 'Facebook'), ('instagram', 'Instagram'), ('search_web', 'Search Web'), ('tik_tok', 'Tik Tok')], default='search_web')
    lead_status = models.CharField(max_length=50, choices=[('new', 'New'), ('contacted', 'Contacted'), ('qualified', 'Qualified')])
    property_type = models.CharField(max_length=50, choices=[('house', 'House'), ('office', 'Office'), ('apartment', 'Apartment')], default='house')

    def create_lead(self, data):
        lead = Lead.objects.create(**data)
        return lead

    def update_lead(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()
        return self

    def change_status(self, new_status):
        self.status = new_status
        self.save()
        return self

    def get_lead_details(self):
        return {
            "lead_source": self.lead_source,
            "status": self.status,
        }

class Deal(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    property = models.ForeignKey(Property,on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=True, blank=True, null=True)
    end_date = models.DateField (auto_now=True, blank=True, null=True)
    content_of_deal = models.TextField (max_length=2000, blank=True, null=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    is_approved = models.BooleanField(default=False, blank=True, null=True)
    deal_type = models.CharField(choices=[('rent', 'Rent'), ('sell', 'Sell')], default='rent')

    def create_deal(self, data):
        deal = Deal.objects.create(**data)
        return deal

    def update_deal(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()
        return self

    def change_is_approved(self, new_status):
        self.is_approved = new_status
        self.save()
        return self

    def get_deal_details(self):
        return {
            "title": self.title,
            "property": self.property,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_approved": self.is_approved,
            "deal_type": self.deal_type,
        }

class SalesClientInteraction(Interaction):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)

    def schedule_follow_up(self, follow_up_date):
        pass

class TheSalesOpportunity(SalesOpportunity):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def change_status(self, new_status):
        self.status = new_status
        self.save()
        return self

    def get_opportunity_details(self):
        return {
            "lead_id": self.lead,
            "property_id": self.property,
            "status": self.status,
        }

class SalesPipeline(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    stages = models.JSONField(blank=True, null=True)
    
    def create_pipeline(self, data):
        pipeline = SalesPipeline.objects.create(**data)
        return pipeline

    def update_pipeline(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()
        return self

    def get_pipeline_details(self):
        return {
            "id": self.id,
            "agent_id": self.agent,
            "stages": self.stages,
        }

    def generate_sales_forecast(self):
        pass

class Collaboration(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    opportunity = models.ForeignKey(TheSalesOpportunity, on_delete=models.CASCADE)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    assigned_tasks = models.JSONField(blank=True, null=True)
    activity_feed = models.JSONField(blank=True, null=True)

    def add_collaboration_note(self, note):
        self.notes += f"\n{note}"
        self.save()

    def assign_task(self, task):
        tasks = self.assigned_tasks
        tasks.append(task)
        self.assigned_tasks = tasks
        self.save()

    def track_task_progress(self, task_id, status):
        tasks = self.assigned_tasks
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = status
                break
        self.assigned_tasks = tasks
        self.save()

    def log_activity(self, activity):
        activities = self.activity_feed
        activities.append(activity)
        self.activity_feed = activities
        self.save()

class SalesAnalytics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    metrics = models.JSONField(blank=True, null=True)
    report_type = models.CharField(max_length=50, blank=True, null=True)

    def generate_report(self, report_type):
        pass

    def analyze_metrics(self):
        pass

    def get_insights(self):
        pass

