from django.db import models
from core.models import User, TimeStampedModel
from django.utils import timezone
from django.core.mail import send_mail
from io import BytesIO
import pandas as pd
from core.models import Report

class AnalyticsReport(Report):
    REPORT_TYPES = (
        ('property_performance', 'Property Performance'),
        ('sales_trend', 'Sales Trend'),
        ('financial_performance', 'Financial Performance'),
        ('client_engagement', 'Client Engagement'),
    )
    type = models.CharField(max_length=50, choices=REPORT_TYPES, default='property_performance')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    filters = models.JSONField(default=dict, blank=True, null=True)
    visualizations = models.JSONField(default=list, blank=True, null=True) 

    def generate_report(self):
        if self.type == 'property_performance':
            return PropertyPerformanceReport.calculate_metrics(self.filters)
        elif self.type == 'sales_trends':
            return SalesTrendReport.analyze_trends(self.filters)
        elif self.type == 'financial_performance':
            return FinancialPerformanceReport.evaluate_investment(self.filters)
        elif self.type == 'client_engagement':
            return ClientEngagementReport.track_engagement(self.filters)
    
    def _fetch_data_based_on_filters(self):
        return {"sample_data": "This should be replaced with actual data"}

    def customize_template(self, new_template):
        self.filters['template'] = new_template
        self.save()

    def add_visualization(self, visualization):
        self.visualizations.append(visualization)
        self.save()

    def get_report_details(self):
        return {
            "id": self.report_id,
            "title": self.title,
            "type": self.type,
            "created_by": self.created_by.username,
            "filters": self.filters,
            "visualizations": self.visualizations,
            "data": self.data,
        }

    def export_report(self, format):
        if format == 'pdf':
            return self._export_to_pdf()
        elif format == 'excel':
            return self._export_to_excel()
        else:
            raise ValueError("Unsupported format")
        
    def _export_to_pdf(self):
        return BytesIO(b"PDF content")

    def _export_to_excel(self):
        df = pd.DataFrame(self.data)
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Report Data')
        buffer.seek(0)
        return buffer

class PropertyPerformanceReport(AnalyticsReport):
    occupancy_rate = models.FloatField(blank=True, null=True)
    average_rental_income = models.FloatField(blank=True, null=True)
    vacancy_rate = models.FloatField(blank=True, null=True)
    maintenance_costs = models.FloatField(blank=True, null=True)
    noi = models.FloatField(blank=True, null=True)  # Net Operating Income

    def calculate_metrics(self):
        self.occupancy_rate = self._calculate_occupancy_rate()
        self.average_rental_income = self._calculate_average_rental_income()
        self.vacancy_rate = self._calculate_vacancy_rate()
        self.maintenance_costs = self._calculate_maintenance_costs()
        self.noi = self._calculate_noi()
        self.save()

    def _calculate_noi(self):
        return self.average_rental_income - self.maintenance_costs

class SalesTrendReport(AnalyticsReport):
    sales_volume = models.FloatField(blank=True, null=True)
    average_selling_price = models.FloatField(blank=True, null=True)
    time_on_market = models.FloatField(blank=True, null=True)
    regional_sales_distribution = models.JSONField(default=dict, blank=True, null=True)

    def analyze_trends(self):
        self.sales_volume = self._calculate_sales_volume()
        self.average_selling_price = self._calculate_average_selling_price()
        self.time_on_market = self._calculate_time_on_market()
        self.regional_sales_distribution = self._calculate_regional_sales_distribution()
        self.save()


class FinancialPerformanceReport(AnalyticsReport):
    rental_income = models.FloatField(blank=True, null=True)
    operating_expenses = models.FloatField(blank=True, null=True)
    cash_flow = models.FloatField(blank=True, null=True)
    roi = models.FloatField(blank=True, null=True)  # Return on Investment

    def evaluate_investment(self):
        self.rental_income = self._calculate_rental_income()
        self.operating_expenses = self._calculate_operating_expenses()
        self.cash_flow = self._calculate_cash_flow()
        self.roi = self._calculate_roi()
        self.save()

    def _calculate_cash_flow(self):
        return self.rental_income - self.operating_expenses

    def _calculate_roi(self):
        return (self.cash_flow / self.operating_expenses) * 100

class ClientEngagementReport(AnalyticsReport):
    lead_conversion_rate = models.FloatField()
    inquiry_response_time = models.FloatField()
    client_satisfaction_score = models.FloatField()

    def track_engagement(self):
        self.lead_conversion_rate = self._calculate_lead_conversion_rate()
        self.inquiry_response_time = self._calculate_inquiry_response_time()
        self.client_satisfaction_score = self._calculate_client_satisfaction_score()
        self.save()

class AutomatedReportScheduler(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    report = models.ForeignKey(AnalyticsReport, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=50, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='daily')
    recipients = models.JSONField(default=list, blank=True, null=True)
    delivery_channel = models.CharField(max_length=50, blank=True, null=True) 
    last_run = models.DateTimeField(null=True, blank=True)

    def schedule_report(self):
        if self.frequency == 'daily':
            next_run = timezone.now() + timezone.timedelta(days=1)
        elif self.frequency == 'weekly':
            next_run = timezone.now() + timezone.timedelta(weeks=1)
        elif self.frequency == 'monthly':
            next_run = timezone.now() + timezone.timedelta(weeks=4)
        else:
            raise ValueError("Unsupported frequency")

        self.last_run = next_run
        self.save()

    def send_report(self):
        report_data = self.report.generate_report()
        for recipient in self.recipients:
            send_mail(
                subject=f"Report: {self.report.name}",
                message=f"Please find the report attached.\n\n{report_data}",
                from_email="smartimo@example.com",
                recipient_list=[recipient]
            )

    def get_schedule_details(self):
        return {
            "id": self.id,
            "report": self.report.title,
            "frequency": self.frequency,
            "recipients": self.recipients,
            "delivery_channel": self.delivery_channel,
            "last_run": self.last_run,
        }

    def update_schedule(self, new_frequency, new_recipients, new_delivery_channel):
        self.frequency = new_frequency
        self.recipients = new_recipients
        self.delivery_channel = new_delivery_channel
        self.save()

    def cancel_schedule(self):
        self.delete()
