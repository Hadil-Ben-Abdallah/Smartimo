from django.db import models
from property_listing.models import RealEstateAgent
from core.models import User, Notification, ClientInteraction, Reminder

class Client(User):
    preferences = models.JSONField(default=dict)
    client_status = models.CharField(max_length=20, choices=[('new', 'New'), ('loyal', 'Loyal'), ('regular', 'Regular')], default='new')
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def log_interaction(self):
        self.save()
    
    def get_interactions(self, client_id):
        return Interaction.objects.filter(client_id=client_id).order_by('-timestamp')

class ClientReminder(Reminder):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    task = models.TextField()
    
    def get_reminders(self, client_id):
        return Reminder.objects.filter(client_id=client_id)

class ClientAnalytics(models.Model):
    client_id = models.OneToOneField(Client, on_delete=models.CASCADE)
    engagement_metrics = models.JSONField(default=dict)
    
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

class ClientRealEstateAgent(RealEstateAgent):
    clients = models.ManyToManyField(Client, related_name='agents')

    def view_clients(self):
        return self.clients.all()
    
    def assign_tag(self, client, tag):
        client.tags.append(tag)
        client.save()
    
    def filter_clients(self, tag):
        return self.clients.filter(tags__contains=[tag])
    
    def receive_notifications(self):
        notifications = []
        notifications = Notification.objects.filter(agent_id=self.id)
        return notifications

