from django.db import models
from core.models import Feedback, TimeStampedModel
from lease_rental_management.models import PropertyManager
from vendor_management.models import Vendor

class VendorRating(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    responsiveness_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    quality_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    deadline_adherence_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    def rate_responsiveness(self, rating):
        self.responsiveness_rating = rating
        self.save()

    def rate_quality(self, rating):
        self.quality_rating = rating
        self.save()

    def rate_deadline_adherence(self, rating):
        self.deadline_adherence_rating = rating
        self.save()

    def calculate_overall_rating(self):
        self.overall_rating = (
            self.responsiveness_rating + self.quality_rating + self.deadline_adherence_rating
        ) / 3
        self.save()
        return self.overall_rating

    def submit_feedback(self, feedback):
        self.feedback = feedback
        self.save()

class VendorPerformance(TimeStampedModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    average_responsiveness_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    average_quality_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    average_deadline_adherence_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    average_overall_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    rating_count = models.IntegerField(default=0)
    performance_trends = models.JSONField(default=dict, blank=True, null=True)

    def update_performance_metrics(self, new_rating: VendorRating):
        self.rating_count += 1
        self.average_responsiveness_rating = (
            (self.average_responsiveness_rating * (self.rating_count - 1)) + new_rating.responsiveness_rating
        ) / self.rating_count
        self.average_quality_rating = (
            (self.average_quality_rating * (self.rating_count - 1)) + new_rating.quality_rating
        ) / self.rating_count
        self.average_deadline_adherence_rating = (
            (self.average_deadline_adherence_rating * (self.rating_count - 1)) + new_rating.deadline_adherence_rating
        ) / self.rating_count
        self.average_overall_rating = (
            (self.average_overall_rating * (self.rating_count - 1)) + new_rating.calculate_overall_rating()
        ) / self.rating_count
        self.save()

    def get_performance_summary(self):
        return {
            "average_responsiveness_rating": self.average_responsiveness_rating,
            "average_quality_rating": self.average_quality_rating,
            "average_deadline_adherence_rating": self.average_deadline_adherence_rating,
            "average_overall_rating": self.average_overall_rating,
            "rating_count": self.rating_count,
            "performance_trends": self.performance_trends,
        }

    def compare_with_others(self, other_vendor_performance):
        comparison = {
            "responsiveness_comparison": self.average_responsiveness_rating - other_vendor_performance.average_responsiveness_rating,
            "quality_comparison": self.average_quality_rating - other_vendor_performance.average_quality_rating,
            "deadline_adherence_comparison": self.average_deadline_adherence_rating - other_vendor_performance.average_deadline_adherence_rating,
            "overall_rating_comparison": self.average_overall_rating - other_vendor_performance.average_overall_rating,
        }
        return comparison

class VendorFeedback(Feedback):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)

    def submit_feedback(self, rating, comments):
        self.rating = rating 
        self.comments = comments
        self.save()

    def view_feedback(self):
        return self.rating, self.comments

class VendorPerformanceDashboard(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    ratings_summary = models.JSONField(default=dict, blank=True, null=True)
    performance_charts = models.JSONField(default=dict, blank=True, null=True)
    comparison_data = models.JSONField(default=dict, blank=True, null=True)
    report_format = models.CharField(max_length=50, choices=[('PDF', 'PDF'), ('Excel', 'Excel')], default='pdf')

    def generate_performance_report(self):
        report = {
            "vendor": self.vendor.id,
            "ratings_summary": self.ratings_summary,
            "performance_charts": self.performance_charts,
            "comparison_data": self.comparison_data,
        }
        if self.report_format == 'PDF':
            report_file_path = f"{self.vendor.name}_performance_report.pdf"
        elif self.report_format == 'Excel':
            report_file_path = f"{self.vendor.name}_performance_report.xlsx"
        return report_file_path

    def view_performance_dashboard(self):
        return {
            "ratings_summary": self.ratings_summary,
            "performance_charts": self.performance_charts,
            "comparison_data": self.comparison_data,
        }

    def customize_dashboard(self, ratings_summary=None, performance_charts=None, comparison_data=None):
        if ratings_summary:
            self.ratings_summary = ratings_summary
        if performance_charts:
            self.performance_charts = performance_charts
        if comparison_data:
            self.comparison_data = comparison_data
        self.save()

