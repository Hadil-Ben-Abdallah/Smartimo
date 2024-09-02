from django.db import models
from django.utils import timezone
from core.models import Report, Property, TimeStampedModel
from property_asset_management.models import MaintenanceTeam

class PropertyMaintenanceTask(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='maintenance_tasks')
    description = models.TextField(blank=True, null=True)
    frequency = models.CharField(max_length=50, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annually', 'Annually')], default='monthly')
    next_scheduled_date = models.DateField(blank=True, null=True)
    responsible_party = models.ForeignKey(MaintenanceTeam, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=50, choices=[('scheduled', 'Scheduled'), ('in-progress', 'In Progress'), ('completed', 'Completed')], default='scheduled')
    notes = models.TextField(blank=True, null=True)

    def create_task(self, property_id, description, frequency, next_scheduled_date, responsible_party_id, status, notes):
        self.property = Property.objects.get(property_id=property_id)
        self.description = description,
        self.frequency = frequency,
        self.next_scheduled_date = next_scheduled_date,
        self.responsible_party = responsible_party_id,
        self.status = status,
        self.notes = notes
        self.save()

    def update_task(self, description, frequency, next_scheduled_date, status, notes):
        self.description = description,
        self.frequency = frequency,
        self.next_scheduled_date = next_scheduled_date,
        self.status = status,
        self.notes = notes
        self.save()

    def delete_task(self):
        self.delete()

    def get_task(self):
        return {
            "id": self.id,
            "property": self.property.property_id,
            "description": self.description,
            "frequency": self.frequency,
            "next_scheduled_date": self.next_scheduled_date,
            "responsible_party": self.responsible_party.id,
            "status": self.status,
            "notes": self.notes
        }

class PropertyMaintenanceReport(Report):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='maintenance_reports')
    total_hours = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    report_date = models.DateField(default=timezone.now, blank=True, null=True)
    labor_costs = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    materials_expenses = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    average_response_time = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def generate_report(self, title, property_id, total_hours, report_date, labor_costs, materials_expenses, average_response_time, completion_rate):
        self.title = title,
        self.property = Property.objects.get(property_id=property_id)
        self.total_hours = total_hours,
        self.report_date = report_date,
        self.labor_costs = labor_costs,
        self.materials_expenses = materials_expenses,
        self.average_response_time = average_response_time,
        self.completion_rate = completion_rate,
        self.save()

    def update_report(self, title, total_hours, report_date, labor_costs, materials_expenses, average_response_time, completion_rate):
        self.title = title,
        self.total_hours = total_hours,
        self.report_date = report_date,
        self.labor_costs = labor_costs,
        self.materials_expenses = materials_expenses,
        self.average_response_time = average_response_time,
        self.completion_rate = completion_rate,
        self.save()

    def delete_report(self):
        self.delete()

    def get_report(self):
        return {
            "title": self.title,
            "property": self.property.property_id,
            "total_hours": self.total_hours,
            "report_date": self.report_date,
            "labor_costs": self.labor_costs,
            "materials_expenses": self.materials_expenses,
            "average_response_time": self.average_response_time,
            "completion_rate": self.completion_rate
        }

