from django.db import models
from core.models import Property, Report, Notification, Communication, Resource, Portal, TimeStampedModel
from property_listing.models import PropertyOwner
from lease_rental_management.models import PropertyManager

class OwnerPortal(Portal):
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)

class OwnerFinancialReport(Report):
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=255, blank=True, null=True)
    document_url = models.URLField(blank=True, null=True)

    def view_report(self):
        return self.document_url

    def download_report(self):
        return f"Downloading report from {self.document_url}"

    def filter_report(self, date_range=None, property=None):
        query = OwnerFinancialReport.objects.filter(owner=self.owner)
        if date_range:
            query = query.filter(created_at__range=date_range)
        if property:
            query = query.filter(property=property)
        return query


class PerformanceMetric(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=255, blank=True, null=True)
    occupancy_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rental_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def view_performance(self):
        return {
            "occupancy_rate": self.occupancy_rate,
            "rental_income": self.rental_income,
            "value": self.value,
            "date": self.date
        }

    def set_performance_goals(self, goals):
        self.performance_goals = goals
        self.save()

    def analyze_performance(self):
        analysis = {
            "occupancy_rate_analysis": self.occupancy_rate * 100,
            "rental_income_analysis": self.rental_income - (self.value * 0.1),
        }
        return analysis

class OwnerNotification(Notification):
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=255, blank=True, null=True)
    delivery_method = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.CharField(max_length=255, blank=True, null=True)

    def customize_preferences(self, preferences):
        self.delivery_method = preferences.get("delivery_method", self.delivery_method)
        self.frequency = preferences.get("frequency", self.frequency)
        self.save()

    def view_notification_history(self):
        return OwnerNotification.objects.filter(owner=self.owner).order_by('-created_at')

class PortalCommunication(Communication):
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    attachments = models.JSONField(default=list, blank=True, null=True)
    communication_log = models.TextField(blank=True, null=True)

    def view_log(self):
        return self.communication_log

    def attach_files(self, files):
        self.attachments.extend(files)
        self.save()

class OwnerResource(Resource):
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)

    def access_resource(self):
        return f"Accessing resources for owner {self.owner}"

    def download_template(self, template_name):
        return f"Downloading template: {template_name}"

    def request_consultation(self):
        return f"Consultation request submitted for owner {self.owner}"

