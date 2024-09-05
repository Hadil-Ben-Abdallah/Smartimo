from django.db import models
from property_listing.models import RealEstateAgent
from core.models import User, ClientInteraction, Reminder, TimeStampedModel, Notification

class Client(User):
    preferences = models.JSONField(default=dict, blank=True, null=True)
    client_status = models.CharField(max_length=20, choices=[('new', 'New'), ('loyal', 'Loyal'), ('regular', 'Regular')], default='new')
    tags = models.JSONField(default=list, blank=True, null=True)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE, related_name="clients")

    def add_client(self, data):
        self.name = data['name']
        self.email = data['email']
        self.phone = data['phone']
        self.address = data['address']
        self.preferences = data.get('preferences', {})
        self.tags = data.get('tags', [])
        self.save()
    
    def update_client(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()
    
    def delete_client(self):
        self.delete()
    
    def get_client(self):
        return self

class Interaction(ClientInteraction):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    
    def log_interaction(self):
        self.save()
    
    def get_interactions(self, client_id):
        return Interaction.objects.filter(client_id=client_id).order_by('-timestamp')

class ClientReminder(Reminder):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    task = models.TextField(blank=True, null=True)
    
    def get_reminders(self, client_id):
        return Reminder.objects.filter(client_id=client_id)

class ClientAnalytics(TimeStampedModel):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    engagement_metrics = models.JSONField(default=dict, blank=True, null=True)
    
    def generate_report(self):
        return self.engagement_metrics
    
    def get_trends(self):
        trends = {}
        for key, value in self.engagement_metrics.items():
            trends[key] = len(value.get('interactions', []))
        return trends
    
    def get_opportunities(self):
        opportunities = []
        if self.engagement_metrics.get('response_rates', 0) < 50:
            opportunities.append("Increase follow-ups with low response rate clients.")
        return opportunities

