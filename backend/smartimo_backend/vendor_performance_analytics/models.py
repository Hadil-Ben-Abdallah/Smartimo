from django.db import models
from django.utils import timezone
from core.models import Property, Feedback, Report, TimeStampedModel
from lease_rental_management.models import Tenant
from vendor_management.models import Vendor

class ServiceRequest(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    photos = models.JSONField(null=True, blank=True)
    preferred_appointment_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('received', 'Received'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('closed', 'Closed')], default='in_progress')
    priority = models.CharField(max_length=50, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low')

    def submit_request(self):
        self.status = 'received'
        self.save()

    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def attach_photos(self, photo_urls):
        self.photos = photo_urls
        self.save()

    def set_priority(self, priority):
        self.priority = priority
        self.save()

    def get_details(self):
        return {
            'id': self.id,
            'property': self.property.property_id,
            'description': self.description,
            'photos': self.photos,
            'preferred_appointment_time': self.preferred_appointment_time,
            'status': self.status,
            'priority': self.priority,
        }


class VendorServicePerformance(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    response_time = models.FloatField(blank=True, null=True)
    resolution_time = models.FloatField(blank=True, null=True)
    customer_satisfaction = models.FloatField(blank=True, null=True)

    def log_response_time(self, vendor_id, service_request_id, response_time):
        performance, created = VendorServicePerformance.objects.get_or_create(
            vendor=vendor_id,
            service_request=service_request_id
        )
        performance.response_time = response_time
        performance.save()

    def log_resolution_time(self, vendor_id, service_request_id, resolution_time):
        performance, created = VendorServicePerformance.objects.get_or_create(
            vendor=vendor_id,
            service_request=service_request_id
        )
        performance.resolution_time = resolution_time
        performance.save()

    def log_customer_satisfaction(self, vendor_id, service_request_id, satisfaction_score):
        performance, created = VendorServicePerformance.objects.get_or_create(
            vendor=vendor_id,
            service_request=service_request_id
        )
        performance.customer_satisfaction = satisfaction_score
        performance.save()

    def get_performance_metrics(self, vendor_id):
        performances = VendorServicePerformance.objects.filter(vendor=vendor_id)
        metrics = {
            'average_response_time': performances.aggregate(models.Avg('response_time'))['response_time__avg'],
            'average_resolution_time': performances.aggregate(models.Avg('resolution_time'))['resolution_time__avg'],
            'average_customer_satisfaction': performances.aggregate(models.Avg('customer_satisfaction'))['customer_satisfaction__avg']
        }
        return metrics

class VendorResponseTime(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    response_time = models.FloatField(blank=True, null=True)

    def calculate_response_time(self, service_request_id):
        try:
            service_request = ServiceRequest.objects.get(id=service_request_id)
            acknowledgment_time = timezone.now()
            response_time = (acknowledgment_time - service_request.created_at).total_seconds() / 3600
            self.response_time = response_time
            self.save()
            return response_time
        except ServiceRequest.DoesNotExist:
            return None

    def get_average_response_time(self, vendor_id):
        response_times = VendorResponseTime.objects.filter(vendor=vendor_id)
        average_response_time = response_times.aggregate(models.Avg('response_time'))['response_time__avg']
        return average_response_time

class VendorResolutionRate(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    resolution_time = models.FloatField(blank=True, null=True)
    within_sla = models.BooleanField(blank=True, null=True)

    def calculate_resolution_rate(self, service_request_id):
        try:
            resolution_time = self.resolution_time
            sla_threshold = 24
            self.within_sla = resolution_time <= sla_threshold
            self.save()
            return resolution_time, self.within_sla
        except ServiceRequest.DoesNotExist:
            return None, None

    def get_resolution_rate(self, vendor_id):
        resolutions = VendorResolutionRate.objects.filter(vendor=vendor_id)
        total_resolutions = resolutions.count()
        sla_compliant_resolutions = resolutions.filter(within_sla=True).count()
        resolution_rate = (sla_compliant_resolutions / total_resolutions * 100) if total_resolutions > 0 else 0
        return resolution_rate

class CustomerFeedback(Feedback):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    customer = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    def collect_feedback(self, vendor_id, service_request_id, satisfaction_score, comments):
        feedback = CustomerFeedback.objects.create(
            vendor=vendor_id,
            service_request=service_request_id,
            satisfaction_score=satisfaction_score,
            comments=comments
        )
        return feedback

    def analyze_feedback(self, vendor_id):
        feedbacks = CustomerFeedback.objects.filter(vendor=vendor_id)
        average_satisfaction = feedbacks.aggregate(models.Avg('satisfaction_score'))['satisfaction_score__avg']
        return average_satisfaction

class VendorPerformanceReport(Report):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    report_period = models.DateTimeField(blank=True, null=True)
    response_times = models.JSONField(blank=True, null=True)
    resolution_rates = models.JSONField(blank=True, null=True)
    performance_scorecard = models.JSONField(blank=True, null=True)

    def generate_report(self, vendor_id, report_period):
        performance = VendorServicePerformance.objects.filter(vendor=vendor_id, created_at__range=(report_period, timezone.now()))
        response_times = performance.aggregate(models.Avg('response_time'))['response_time__avg']
        resolution_rates = performance.aggregate(models.Avg('resolution_time'))['resolution_time__avg']
        satisfaction_scores = performance.aggregate(models.Avg('customer_satisfaction'))['customer_satisfaction__avg']

        self.response_times = {'average_response_time': response_times}
        self.resolution_rates = {'average_resolution_rate': resolution_rates}
        self.performance_scorecard = {'average_satisfaction_score': satisfaction_scores}
        self.save()

    def customize_report(self, report_id, filters):
        pass

    def export_report(self, report_id, format):
        pass

class VendorPerformanceAlert(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=50, blank=True, null=True)
    threshold_value = models.FloatField(blank=True, null=True)
    current_value = models.FloatField(blank=True, null=True)
    severity_level = models.CharField(max_length=50, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low')
    notification_settings = models.JSONField(blank=True, null=True)

    def create_alert(self, vendor_id, metric_type, threshold_value, severity_level):
        self.vendor = vendor_id
        self.metric_type = metric_type
        self.threshold_value = threshold_value
        self.severity_level = severity_level
        self.save()

    def send_alert(self, alert_id):
        alert = VendorPerformanceAlert.objects.get(id=alert_id)
        pass

    def customize_notification_settings(self, alert_id, settings):
        alert = VendorPerformanceAlert.objects.get(id=alert_id)
        alert.notification_settings = settings
        alert.save()