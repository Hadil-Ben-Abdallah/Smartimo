from django.db import models
from client_management.models import Client
from core.models import Property
from django.core.exceptions import ValidationError
import requests
from django.utils import timezone

class CRMIntegration(models.Model):
    id = models.AutoField(primary_key=True)
    crm_tool = models.CharField(max_length=100, choices=[('salesforce', 'Salesforce'), ('hubSpot', 'HubSpot')], default='salesforce')
    api_key = models.CharField(max_length=255)
    sync_status = models.CharField(max_length=50, choices=[('active', 'Active'), ('paused', 'Paused'), ('failed', 'Failed')], default='paused')
    last_sync_time = models.DateTimeField(null=True, blank=True)

    def sync_data(self):
        if self.crm_tool == 'Salesforce':
            url = 'https://api.salesforce.com/v1/sync'
        elif self.crm_tool == 'HubSpot':
            url = 'https://api.hubspot.com/v1/sync'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            self.sync_status = 'success'
        else:
            self.sync_status = 'failed'
        self.last_sync_time = timezone.now()
        self.save()

    def check_sync_status(self):
        return {
            'status': self.sync_status,
            'last_sync_time': self.last_sync_time
        }

    def resolve_conflicts(self):
        conflicts = self.get_conflicts()  # this method retrieves conflicts
        for conflict in conflicts:
            self.resolve_conflict(conflict)  # this method resolves individual conflicts
        self.sync_data()  # Retry synchronization after resolving conflicts

    def update_credentials(self, new_api_key):
        self.api_key = new_api_key
        self.save()

    def get_conflicts(self):
        # method to get conflicts
        return []
    
    def resolve_conflict(self, conflict):
        # method to resolve individual conflicts
        pass

class CRMClientSync(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    crm_client_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    sync_status = models.CharField(max_length=50, choices=[('active', 'Active'), ('paused', 'Paused'), ('failed', 'Failed')], default='paused')

    def export_client(self):
        crm_tool = CRMIntegration.objects.get(id=self.integration_id).crm_tool


        if crm_tool == 'Salesforce':
            url = f'https://api.salesforce.com/v1/clients/{self.crm_client_id}'
        elif crm_tool == 'HubSpot':
            url = f'https://api.hubspot.com/v1/clients/{self.crm_client_id}'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.get_crm_api_key()}',
            'Content-Type': 'application/json'
        }

        data = {
            'name': Client.username,
            'email': Client.email,
            'phone': Client.phone,
            'address': Client.address
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            self.sync_status = 'success'
        else:
            self.sync_status = 'failed'
        self.last_update_time = timezone.now()
        self.save()

    def import_client(self):
        crm_tool = CRMIntegration.objects.get(id=self.integration_id).crm_tool

        if crm_tool == 'Salesforce':
            url = f'https://api.salesforce.com/v1/clients/{self.crm_client_id}'
        elif crm_tool == 'HubSpot':
            url = f'https://api.hubspot.com/v1/clients/{self.crm_client_id}'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.get_crm_api_key()}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            client_data = response.json()
            self.client.name = client_data['name']
            self.client.email = client_data['email']
            self.client.phone = client_data['phone']
            self.client.address = client_data['address']
            self.client.save()
            self.sync_status = 'success'
        else:
            self.sync_status = 'failed'
        self.last_update_time = timezone.now()
        self.save()

    def resolve_conflict(self):
        # resolve conflicts during synchronization
        self.import_client() # Retry import after conflict resolution


class CRMSalesOpportunity(models.Model):
    id = models.AutoField(primary_key=True)
    crm_opportunity_id = models.CharField(max_length=100)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    stage = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    probability = models.DecimalField(max_digits=5, decimal_places=2)

    def create_opportunity(self):
        crm_tool = CRMIntegration.objects.get(id=self.integration_id).crm_tool

        if crm_tool == 'Salesforce':
            url = 'https://api.salesforce.com/v1/opportunities'
        elif crm_tool == 'HubSpot':
            url = 'https://api.hubspot.com/v1/opportunities'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.get_crm_api_key()}',
            'Content-Type': 'application/json'
        }

        data = {
            'property': Property.property_id,
            'stage': self.stage,
            'value': self.value,
            'probability': self.probability
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            self.crm_opportunity_id = response.json().get('id')
            self.save()
        else:
            raise ValidationError("Failed to create opportunity in CRM")

    def update_opportunity(self):
        crm_tool = CRMIntegration.objects.get(id=self.integration_id).crm_tool
        
        if crm_tool == 'Salesforce':
            url = f'https://api.salesforce.com/v1/opportunities/{self.crm_opportunity_id}'
        elif crm_tool == 'HubSpot':
            url = f'https://api.hubspot.com/v1/opportunities/{self.crm_opportunity_id}'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.get_crm_api_key()}',
            'Content-Type': 'application/json'
        }

        data = {
            'stage': self.stage,
            'value': self.value,
            'probability': self.probability
        }

        response = requests.put(url, headers=headers, json=data)
        if response.status_code != 200:
            raise ValidationError("Failed to update opportunity in CRM")

    def track_opportunity(self):
        crm_tool = CRMIntegration.objects.get(id=self.integration_id).crm_tool
        
        if crm_tool == 'Salesforce':
            url = f'https://api.salesforce.com/v1/opportunities/{self.crm_opportunity_id}'
        elif crm_tool == 'HubSpot':
            url = f'https://api.hubspot.com/v1/opportunities/{self.crm_opportunity_id}'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.get_crm_api_key()}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            opportunity_data = response.json()
            self.stage = opportunity_data.get('stage')
            self.value = opportunity_data.get('value')
            self.probability = opportunity_data.get('probability')
            self.save()
        else:
            raise ValidationError("Failed to track opportunity in CRM")

class CRMClientInteraction(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50, choices=[('call', 'Call'), ('email', 'Email'), ('meeting', 'Meeting')], default='call')
    details = models.TextField()

    def log_interaction(self):
        crm_tool = CRMIntegration.objects.get(id=self.integration_id).crm_tool
        
        if crm_tool == 'Salesforce':
            url = 'https://api.salesforce.com/v1/interactions'
        elif crm_tool == 'HubSpot':
            url = 'https://api.hubspot.com/v1/interactions'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.get_crm_api_key()}',
            'Content-Type': 'application/json'
        }

        data = {
            'client': self.client.username,
            'interaction_type': self.interaction_type,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 201:
            raise ValidationError("Failed to log interaction in CRM")

    def link_to_opportunity(self, opportunity_id):
        crm_tool = CRMIntegration.objects.get(id=self.integration_id).crm_tool
        
        if crm_tool == 'Salesforce':
            url = f'https://api.salesforce.com/v1/opportunities/{opportunity_id}/interactions'
        elif crm_tool == 'HubSpot':
            url = f'https://api.hubspot.com/v1/opportunities/{opportunity_id}/interactions'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.get_crm_api_key()}',
            'Content-Type': 'application/json'
        }

        data = {
            'interaction_id': self.id
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise ValidationError("Failed to link interaction to opportunity in CRM")

    def schedule_followup(self):
        crm_tool = CRMIntegration.objects.get(id=self.integration_id).crm_tool
        
        if crm_tool == 'Salesforce':
            url = 'https://api.salesforce.com/v1/followups'
        elif crm_tool == 'HubSpot':
            url = 'https://api.hubspot.com/v1/followups'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.get_crm_api_key()}',
            'Content-Type': 'application/json'
        }

        data = {
            'client': self.client.user_id,
            'followup_time': self.timestamp.isoformat()
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 201:
            raise ValidationError("Failed to schedule follow-up in CRM")

class CRMClientSegmentation(models.Model):
    id = models.AutoField(primary_key=True)
    segment_name = models.CharField(max_length=100)
    criteria = models.TextField()
    client_list = models.JSONField()  # List of client IDs

    def create_segment(self):
        crm_tool = CRMIntegration.objects.get(id=self.integration_id).crm_tool
        
        if crm_tool == 'Salesforce':
            url = 'https://api.salesforce.com/v1/segments'
        elif crm_tool == 'HubSpot':
            url = 'https://api.hubspot.com/v1/segments'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.get_crm_api_key()}',
            'Content-Type': 'application/json'
        }

        data = {
            'segment_name': self.segment_name,
            'criteria': self.criteria
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            self.id = response.json().get('id')
            self.save()
        else:
            raise ValidationError("Failed to create segment in CRM")

    def update_segment(self):
        crm_tool = CRMIntegration.objects.get(id=self.integration_id).crm_tool
        
        if crm_tool == 'Salesforce':
            url = f'https://api.salesforce.com/v1/segments/{self.id}'
        elif crm_tool == 'HubSpot':
            url = f'https://api.hubspot.com/v1/segments/{self.id}'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.get_crm_api_key()}',
            'Content-Type': 'application/json'
        }

        data = {
            'criteria': self.criteria
        }

        response = requests.put(url, headers=headers, json=data)
        if response.status_code != 200:
            raise ValidationError("Failed to update segment in CRM")

    def execute_campaign(self):
        crm_tool = CRMIntegration.objects.get(id=self.integration_id).crm_tool
        
        if crm_tool == 'Salesforce':
            url = 'https://api.salesforce.com/v1/campaigns'
        elif crm_tool == 'HubSpot':
            url = 'https://api.hubspot.com/v1/campaigns'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.get_crm_api_key()}',
            'Content-Type': 'application/json'
        }

        data = {
            'segment_id': self.id,
            'message': 'Targeted campaign message'
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 201:
            raise ValidationError("Failed to execute campaign in CRM")

class CRMIntegrationSettings(models.Model):
    id = models.AutoField(primary_key=True)
    crm_tool = models.CharField(max_length=100)
    custom_fields = models.JSONField()
    sync_frequency = models.CharField(max_length=50, choices=[('hourly', 'Hourly'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='hourly')
    notification_settings = models.JSONField()

    def configure_integration(self):
        crm_tool = self.crm_tool
        
        if crm_tool == 'Salesforce':
            url = 'https://api.salesforce.com/v1/configure'
        elif crm_tool == 'HubSpot':
            url = 'https://api.hubspot.com/v1/configure'
        else:
            raise ValidationError("Unsupported CRM tool")

        headers = {
            'Authorization': f'Bearer {self.get_crm_api_key()}',
            'Content-Type': 'application/json'
        }

        data = {
            'custom_fields': self.custom_fields,
            'sync_frequency': self.sync_frequency,
            'notification_settings': self.notification_settings
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise ValidationError("Failed to configure CRM integration")

    def set_sync_frequency(self, frequency):
        self.sync_frequency = frequency
        self.save()

    def update_notifications(self, settings):
        self.notification_settings = settings
        self.save()

