from django.db import models
from django.utils import timezone
from lease_rental_management.models import Tenant

class CommunicationTemplate(models.Model):
    
    id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=255, blank=True, null=True)
    template_type = models.CharField(max_length=10, choices=[('email', 'Email'), ('sms', 'SMS')], default='email')
    content = models.TextField(blank=True, null=True)
    placeholders = models.JSONField(blank=True, null=True)
    branding_elements = models.JSONField(blank=True, null=True)

    def create_template(self, template_name, template_type, content, placeholders, branding_elements):
        new_template = CommunicationTemplate.objects.create(
            template_name=template_name,
            template_type=template_type,
            content=content,
            placeholders=placeholders,
            branding_elements=branding_elements
        )
        return new_template

    def edit_template(self, template_name=None, content=None, placeholders=None, branding_elements=None):
        if template_name:
            self.template_name = template_name
        if content:
            self.content = content
        if placeholders:
            self.placeholders = placeholders
        if branding_elements:
            self.branding_elements = branding_elements
        self.save()
        return self

    def delete_template(self):
        self.delete()

    def view_template(self):
        return {
            "template_id": self.id,
            "template_name": self.template_name,
            "template_type": self.template_type,
            "content": self.content,
            "placeholders": self.placeholders,
            "branding_elements": self.branding_elements
        }

    def customize_template(self, placeholders_values, branding_elements):
        customized_content = self.content
        for placeholder, value in placeholders_values.items():
            customized_content = customized_content.replace(f"{{{{{placeholder}}}}}", value)
        customized_branding = self.branding_elements.copy()
        customized_branding.update(branding_elements)
        return {
            "customized_content": customized_content,
            "customized_branding": customized_branding
        }

    @classmethod
    def list_templates(cls):
        return cls.objects.all()


class CommunicationWorkflow(models.Model):
    id = models.AutoField(primary_key=True)
    template = models.ForeignKey(CommunicationTemplate, on_delete=models.CASCADE)
    event_trigger = models.CharField(max_length=255, blank=True, null=True)
    schedule = models.JSONField(blank=True, null=True)
    recipient_list = models.ManyToManyField(Tenant, blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive')

    def create_workflow(self, template, event_trigger, schedule, recipient_list, status='active'):
        workflow = CommunicationWorkflow.objects.create(
            template=template,
            event_trigger=event_trigger,
            schedule=schedule,
            status=status
        )
        workflow.recipient_list.set(recipient_list)
        workflow.save()
        return workflow

    def edit_workflow(self, event_trigger=None, schedule=None, recipient_list=None, status=None):
        if event_trigger:
            self.event_trigger = event_trigger
        if schedule:
            self.schedule = schedule
        if recipient_list:
            self.recipient_list.set(recipient_list)
        if status:
            self.status = status
        self.save()
        return self

    def delete_workflow(self):
        self.delete()

    def view_workflow(self):
        return {
            "workflow_id": self.id,
            "template": self.template.view_template(),
            "event_trigger": self.event_trigger,
            "schedule": self.schedule,
            "recipient_list": list(self.recipient_list.all().values('username', 'email')),
            "status": self.status
        }

    @classmethod
    def list_workflows(cls):
        return cls.objects.all()

    def schedule_workflow(self):

        pass

    def execute_workflow(self):
        pass


class TenantCommunicationLog(models.Model):
    id = models.AutoField(primary_key=True)
    workflow = models.ForeignKey(CommunicationWorkflow, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=20, choices=[('sent', 'Sent'), ('failed', 'Failed')], default='sent')
    open_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True, null=True)
    click_through_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True, null=True)
    response_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, blank=True, null=True)
    sent_at = models.DateTimeField(default=timezone.now)

    def log_communication(self, workflow, recipient, delivery_status, open_rate=0.00, click_through_rate=0.00, response_rate=0.00):
        log = TenantCommunicationLog.objects.create(
            workflow=workflow,
            recipient=recipient,
            delivery_status=delivery_status,
            open_rate=open_rate,
            click_through_rate=click_through_rate,
            response_rate=response_rate
        )
        return log

    def view_log(self):
        return {
            "log_id": self.id,
            "workflow": self.workflow.view_workflow(),
            "recipient": self.recipient.username,
            "delivery_status": self.delivery_status,
            "open_rate": self.open_rate,
            "click_through_rate": self.click_through_rate,
            "response_rate": self.response_rate,
            "sent_at": self.sent_at
        }

    @classmethod
    def list_logs(cls):
        return cls.objects.all()

    def generate_report(self):
        pass

    def track_metrics(self):
        pass


class CommunicationAnalytics(models.Model):
    id = models.AutoField(primary_key=True)
    log = models.ForeignKey(TenantCommunicationLog, on_delete=models.CASCADE)
    open_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    click_through_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    response_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    engagement_metrics = models.JSONField(blank=True, null=True)

    def analyze_performance(self):
        pass

    def generate_analytics_report(self):
        pass

    def view_analytics(self):
        return {
            "analytics_id": self.id,
            "log": self.log.view_log(),
            "open_rate": self.open_rate,
            "click_through_rate": self.click_through_rate,
            "response_rate": self.response_rate,
            "engagement_metrics": self.engagement_metrics
        }

    @classmethod
    def list_analytics(cls):
        return cls.objects.all()


class TemplateVersionControl(models.Model):
    id = models.AutoField(primary_key=True)
    template = models.ForeignKey(CommunicationTemplate, on_delete=models.CASCADE)
    version_number = models.IntegerField(blank=True, null=True)
    changes = models.TextField(blank=True, null=True)

    def create_version(self, template, changes):
        version_number = TemplateVersionControl.objects.filter(template=template).count() + 1
        version = TemplateVersionControl.objects.create(
            template=template,
            version_number=version_number,
            changes=changes
        )
        return version

    def view_version(self):
        return {
            "version_id": self.id,
            "template": self.template.view_template(),
            "version_number": self.version_number,
            "changes": self.changes
        }

    @classmethod
    def list_versions(cls, template):
        return cls.objects.filter(template=template)

    def rollback_version(self, version_number):
        previous_version = TemplateVersionControl.objects.get(template=self.template, version_number=version_number)
        self.template.content = previous_version.changes
        self.template.save()

    def track_changes(self):
        pass

