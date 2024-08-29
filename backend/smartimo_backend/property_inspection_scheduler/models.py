from django.db import models
from core.models import Property, User, Reminder, Report, Communication, Notification
from remote_property_monitoring.models import Inspector


class InspectionSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    inspection_frequency = models.CharField(max_length=50, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annually', 'Annually')], default='monthly')
    inspection_criteria = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(Inspector, on_delete=models.SET_NULL, null=True)
    customization = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(null=True, blank=True)

    def schedule_inspection(self, inspection_date):
        InspectionTask.objects.create(
            schedule_id=self,
            assigned_to=self.assigned_to,
            status='scheduled',
            inspection_date=inspection_date,
            checklist_results='',
            notes=''
        )

    def update_schedule(self, frequency=None, criteria=None, assigned_to=None, start_date=None, end_date=None):
        if frequency:
            self.inspection_frequency = frequency
        if criteria:
            self.inspection_criteria = criteria
        if assigned_to:
            self.assigned_to = assigned_to
        if start_date:
            self.start_date = start_date
        if end_date:
            self.end_date = end_date
        self.save()

    def assign_inspection_task(self, inspector):
        self.assigned_to = inspector
        self.save()

    def customize_schedule(self, customization):
        self.customization = customization
        self.save()


class PropertyInspectionReminder(Reminder):
    schedule = models.ForeignKey(InspectionSchedule, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Inspector, on_delete=models.CASCADE)

    def configure_reminder_settings(self):
        Reminder.objects.create(
            schedule=self.schedule,
            recipient=self.recipient,
            frequency=self.frequency,
            channel=self.delivary_channel
        )


class InspectionTask(models.Model):
    id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(InspectionSchedule, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Inspector, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=[('scheduled', 'Scheduled'), ('in-progress', 'In Progress'), ('completed', 'Completed')], default='scheduled')
    inspection_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(null=True, blank=True)
    checklist_results = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def view_assigned_tasks(self):
        return InspectionTask.objects.filter(assigned_to=self.assigned_to)

    def update_task_status(self, status, completion_date=None):
        self.status = status
        if completion_date:
            self.completion_date = completion_date
        self.save()

    def log_results(self, results, notes):
        self.checklist_results = results
        self.notes = notes
        self.update_task_status('completed', completion_date=models.DateField.auto_now)

    def communicate_with_manager(self, message):
        Communication.objects.create(
            message=message,
            date=models.DateTimeField.auto_now,
            communication=self.assigned_to
        )


class PropertyInspectionReport(Report):
    schedule = models.ForeignKey(InspectionSchedule, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    inspection_date = models.DateField(blank=True, null=True)
    findings = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    report_summary = models.TextField(blank=True, null=True)

    def generate_report(self):
        self.report_summary = f"Inspection Summary for Property {self.property.address} on {self.inspection_date}"
        self.save()

    def send_report(self, recipient):
        Notification.objects.create(
            user=recipient,
            message=f"Inspection Report for {self.property.address} is ready.",
            date=models.DateTimeField.auto_now,
            status='sent'
        )

    def view_report(self):
        return {
            'schedule': self.schedule.id,
            'property': self.property.property_id,
            'inspection_date': self.inspection_date,
            'findings': self.findings,
            'recommendations': self.recommendations,
            'report_summary': self.report_summary
        }

    def customize_report(self, custom_format):
        self.report_summary = f"Customized Report: {custom_format}"
        self.save()


class InspectionAnalytics(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    period = models.CharField(max_length=50, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annually', 'Annually')], default='monthly')
    completion_rate = models.FloatField(blank=True, null=True)
    compliance_level = models.FloatField(blank=True, null=True)
    findings_summary = models.TextField(blank=True, null=True)

    def generate_inspection_metrics(self):
        self.completion_rate = InspectionTask.objects.filter(status='completed').count() / \
                                InspectionTask.objects.filter(schedule__property=self.property.property_id).count()
        self.save()

    def track_inspection_progress(self):
        return {
            'completed': InspectionTask.objects.filter(status='completed').count(),
            'in_progress': InspectionTask.objects.filter(status='in progress').count(),
            'pending': InspectionTask.objects.filter(status='scheduled').count()
        }

    def get_compliance_report(self):
        return {
            'compliance_level': self.compliance_level,
            'compliance_issues': "No significant issues" if self.compliance_level > 0.9 else "Review required"
        }

    def analyze_inspection_trends(self):
        return {
            'increase_in_issues': True,
            'common_issues': ["Issue1", "Issue2"]
        }

