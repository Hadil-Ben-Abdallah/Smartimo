from django.db import models
from core.models import User, Notification
from vendor_management.models import Vendor
from datetime import datetime, timedelta

class WorkflowStep(models.Model):
    id = models.AutoField(primary_key=True)
    step_name = models.CharField(max_length=255, blank=True, null=True)
    task = models.TextField(blank=True, null=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_steps', null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='assigned_steps', null=True, blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('in-progress', 'In Progress'), ('completed', 'Completed')], default='pending')

    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def assign_task(self, user=None, vendor=None):
        if user:
            self.assignee = user
        if vendor:
            self.vendor = vendor
        self.save()

    def set_due_date(self, new_due_date):
        self.due_date = new_due_date
        self.save()

class Trigger(models.Model):
    id = models.AutoField(primary_key=True)
    trigger_type = models.CharField(max_length=50, choices=[('time-based', 'Time-Based'), ('event-based', 'Event-Based')], default='time-based')
    condition = models.TextField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)

    def create_trigger(self, trigger_type, condition, action):
        self.trigger_type = trigger_type
        self.condition = condition
        self.action = action
        self.save()

    def update_condition(self, new_condition):
        self.condition = new_condition
        self.save()

    def set_action(self, new_action):
        self.action = new_action
        self.save()

class Workflow(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    steps = models.ManyToManyField(WorkflowStep, related_name='workflows', blank=True, null=True)
    triggers = models.ManyToManyField(Trigger, related_name='workflows', blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive')

    def create_step(self, step_name, task, assignee=None, vendor=None, due_date=None):
        new_step = WorkflowStep.objects.create(step_name=step_name, task=task, due_date=due_date or datetime.now() + timedelta(days=7))
        if assignee:
            new_step.assign_task(user=assignee)
        if vendor:
            new_step.assign_task(vendor=vendor)
        self.steps.add(new_step)

    def configure_trigger(self, trigger_type, condition, action):
        new_trigger = Trigger.objects.create(trigger_type=trigger_type, condition=condition, action=action)
        self.triggers.add(new_trigger)

    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def view_progress(self):
        completed_steps = self.steps.filter(status='completed').count()
        total_steps = self.steps.count()
        return {
            'completed_steps': completed_steps,
            'total_steps': total_steps,
            'progress_percentage': (completed_steps / total_steps) * 100 if total_steps > 0 else 0
        }

class TaskTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=255, blank=True, null=True)
    tasks = models.ManyToManyField(WorkflowStep, related_name='templates', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def create_task(self, step_name, task_description, due_date=None):
        new_task = WorkflowStep.objects.create(step_name=step_name, task=task_description, due_date=due_date or datetime.now() + timedelta(days=7))
        self.tasks.add(new_task)

    def apply_template(self, workflow):
        for task in self.tasks.all():
            workflow.steps.add(task)

    def update_template(self, step_name, new_task_description=None, new_name=None):
        task = self.tasks.filter(step_name=step_name).first()
        if task:
            if new_name:
                self.template_name = new_name
            if new_task_description:
                self.description = new_task_description
            task.save()

class WorkflowPerformanceMetric(models.Model):
    id = models.AutoField(primary_key=True)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='metrics')
    metric_name = models.CharField(max_length=255, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    def record_metric(self, value):
        self.value = value
        self.save()

    def generate_report(self):
        return {
            'workflow_name': self.workflow.name,
            'metric_name': self.metric_name,
            'value': self.value
        }

    def analyze_performance(self):
        metrics = WorkflowPerformanceMetric.objects.filter(workflow=self.workflow)
        total_value = sum(metric.value for metric in metrics)
        average_value = total_value / metrics.count() if metrics.exists() else 0
        return {
            'workflow': self.workflow.name,
            'average_metric_value': average_value
        }

class WorkflowNotification(Notification):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    triggered_by = models.ForeignKey(Trigger, on_delete=models.CASCADE, related_name='notifications', blank=True, null=True)

    def update_status(self, new_status):
        self.triggered_by.update_condition(new_status)

    def set_recipient(self, user=None, vendor=None):
        if user:
            self.recipient = user
        if vendor:
            self.vendor = vendor
        self.save()
