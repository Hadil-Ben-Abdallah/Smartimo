from django.db import models
from django.utils import timezone
from core.models import Notification
from visitor_management_for_property_access.models import Visitor

class TenantVisitor(Visitor):
    expected_arrival_time = models.DateTimeField(blank=True, null=True)
    visitor_pass = models.CharField(max_length=255, null=True, blank=True)
    expected_arrival_time = models.DateField(null=True, blank=True)

    def pre_register_visitor(self, visitor_id, visitor_name, visitor_email, visitor_phone, purpose, expected_arrival_time):
        self.id = visitor_id
        self.name = visitor_name
        self.email = visitor_email
        self.phone = visitor_phone
        self.visit_purpose = purpose
        self.expected_arrival_time = expected_arrival_time
        self.save()
        return self.generate_visitor_pass()

    def send_confirmation_notification(self):
        print(f"Notification sent to tenant and visitor for visitor pass: {self.visitor_pass}")

    def update_visitor_details(self, new_arrival_time=None, new_email=None, new_phone=None):
        if new_arrival_time:
            self.expected_arrival_time = new_arrival_time
        if new_email:
            self.email = new_email
        if new_phone:
            self.phone = new_phone
        self.save()

    def generate_visitor_pass(self):
        self.visitor_pass = f"PASS-{self.id}-{self.expected_arrival_time.strftime('%Y%m%d%H%M')}"
        self.save()
        self.send_confirmation_notification()
        return self.visitor_pass

class CheckInCheckOut(models.Model):
    visitor = models.ForeignKey(TenantVisitor, on_delete=models.CASCADE)
    checkin_time = models.DateTimeField(null=True, blank=True)
    checkout_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('checked-in', 'Checked-In'), ('checked-out', 'Checked-Out')], default='checked-in')

    def check_in(self):
        self.checkin_time = timezone.now()
        self.status = "checked-in"
        self.save()
        return self.get_checkin_checkout_details()

    def check_out(self):
        self.checkout_time = timezone.now()
        self.status = "checked-out"
        self.save()
        return self.get_checkin_checkout_details()

    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def get_checkin_checkout_details(self):
        return {
            "checkin_time": self.checkin_time,
            "checkout_time": self.checkout_time,
            "status": self.status,
            "visitor_pass": self.visitor.visitor_pass
        }

class SecurityNotification(Notification):
    visitor = models.ForeignKey(TenantVisitor, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=100, blank=True, null=True)
    triggered_at = models.DateTimeField(blank=True, null=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def configure_alert_rules(self, alert_type, rule_details):
        self.alert_type = alert_type
        print(f"Configured alert rules: {rule_details}")

    def log_alert_activity(self):
        print(f"Alert triggered: {self.alert_type} at {self.triggered_at}")

    def resolve_alert(self):
        self.resolved_at = timezone.now()
        self.save()
        print(f"Alert resolved at {self.resolved_at}")

class VisitorLog(models.Model):
    id = models.AutoField(primary_key=True)
    visitor = models.ForeignKey(TenantVisitor, on_delete=models.CASCADE)
    checkin = models.ForeignKey(CheckInCheckOut, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    activity = models.TextField(blank=True, null=True)
    host_information = models.CharField(max_length=255, blank=True, null=True)
    access_permissions = models.CharField(max_length=255, blank=True, null=True)

    def record_activity(self, activity_description):
        self.activity = activity_description
        self.timestamp = timezone.now()
        self.save()

    def generate_activity_report(self):
        print(f"Generated report for visitor {self.visitor.visitor_pass}")

    def view_activity_log(self):
        return {
            "timestamp": self.timestamp,
            "activity": self.activity,
            "host_information": self.host_information,
            "access_permissions": self.access_permissions
        }

    def retrieve_historical_logs(self, visitor_id):
        return VisitorLog.objects.filter(id=visitor_id).order_by('-timestamp')

class AccessControlIntegration(models.Model):
    id = models.AutoField(primary_key=True)
    system_name = models.CharField(max_length=255, blank=True, null=True)
    entry_points = models.JSONField(blank=True, null=True)
    access_rules = models.JSONField(blank=True, null=True)
    visitor = models.ForeignKey(TenantVisitor, on_delete=models.CASCADE)
    checkin = models.ForeignKey(CheckInCheckOut, on_delete=models.CASCADE)

    def enforce_access_policies(self):
        print(f"Access policies enforced for visitor {self.visitor.visitor_pass} at entry points {self.entry_points}")

    def configure_access_rules(self, new_rules):
        self.access_rules = new_rules
        self.save()

    def synchronize_with_access_system(self):
        print(f"Data synchronized with access control system: {self.system_name}")

    def validate_access(self):
        if self.checkin.status == "checked-in":
            print(f"Access validated for visitor {self.visitor.visitor_pass}")
        else:
            print(f"Access denied for visitor {self.visitor.visitor_pass}")

