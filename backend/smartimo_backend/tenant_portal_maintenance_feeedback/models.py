from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from lease_rental_management.models import Tenant
from tenant_portal_maintenance_tracking.models import MaintenanceFeedback
from maintenance_and_service_requests.models import MaintenanceRequest
from lease_rental_management.models import PropertyManager

class TenantMaintenanceFeedback(MaintenanceFeedback):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    service_request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE)
    maintenance_issue_type = models.CharField(max_length=255, blank=True, null=True)
    service_date = models.DateField(auto_now_add=True, blank=True, null=True)
    rating_timeliness = models.PositiveSmallIntegerField(blank=True, null=True)
    rating_professionalism = models.PositiveSmallIntegerField(blank=True, null=True)
    rating_quality = models.PositiveSmallIntegerField(blank=True, null=True)
    rating_overall_satisfaction = models.PositiveSmallIntegerField(blank=True, null=True)

    def submit_feedback(self):
        self.save()
        self.notify_property_manager()
    
    def edit_feedback(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()

    def view_feedback(self):
        return {
            "tenant": self.tenant.username,
            "service_request": self.service_request.issue_type,
            "maintenance_issue_type": self.maintenance_issue_type,
            "service_date": self.service_date,
            "comments": self.comments,
            "ratings": {
                "timeliness": self.rating_timeliness,
                "professionalism": self.rating_professionalism,
                "quality": self.rating_quality,
                "overall_satisfaction": self.rating_overall_satisfaction,
            },
        }

    @classmethod
    def filter_feedback(cls, **filters):
        return cls.objects.filter(**filters)

    @classmethod
    def generate_feedback_report(cls):
        feedbacks = cls.objects.all()
        report = {
            "total_feedbacks": feedbacks.count(),
            "average_ratings": {
                "timeliness": feedbacks.aggregate(models.Avg('rating_timeliness'))['rating_timeliness__avg'],
                "professionalism": feedbacks.aggregate(models.Avg('rating_professionalism'))['rating_professionalism__avg'],
                "quality": feedbacks.aggregate(models.Avg('rating_quality'))['rating_quality__avg'],
                "overall_satisfaction": feedbacks.aggregate(models.Avg('rating_overall_satisfaction'))['rating_overall_satisfaction__avg'],
            },
            "feedbacks_details": [
                {
                    "rating": feedback.rating,
                    "tenant": feedback.tenant.username,
                    "service_request": feedback.service_request.issue_type,
                    "maintenance_issue_type": feedback.maintenance_issue_type,
                    "service_date": feedback.service_date,
                    "ratings": {
                        "timeliness": feedback.rating_timeliness,
                        "professionalism": feedback.rating_professionalism,
                        "quality": feedback.rating_quality,
                        "overall_satisfaction": feedback.rating_overall_satisfaction,
                    },
                    "comments": feedback.comments,
                } for feedback in feedbacks
            ]
        }
        return report

    def notify_property_manager(self):
        property_manager_email = PropertyManager.email
        subject = "New Maintenance Feedback Submitted"
        message = (
            f"Dear Property Manager {PropertyManager.username},\n\n"
            f"A new feedback has been submitted by {self.tenant.username} "
            f"regarding the service request: {self.service_request.issue_type}.\n\n"
            f"Please review the feedback and take the necessary action.\n\n"
            f"Thank you,\n"
            f"The Smartimo Team"
        )

        send_mail(
            subject,
            message,
            [property_manager_email],
            fail_silently=False,
        )

        return f"Notification sent to {property_manager_email}: {subject}"

    def __str__(self):
        return f"Feedback by {self.tenant.username} for {self.maintenance_issue_type}"

