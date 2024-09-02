from django.db import models
from core.models import Category, Report, TimeStampedModel
from property_portfolio_risk_management.models import RiskAssessment

class RiskCategory(Category):
    risk_criteria = models.JSONField(blank=True, null=True)

    def create_category(self, criteria, name , description):
        self.name = name 
        self.description = description
        self.risk_criteria = criteria
        self.save()

    def get_category(self):
        return {
            "id": self.category_id,
            "name": self.name,
            "description": self.description,
            "risk_criteria": self.risk_criteria,
        }


class KeyRiskIndicator(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    risk_assessment = models.ForeignKey(RiskAssessment, on_delete=models.CASCADE)
    indicator_name = models.CharField(max_length=255, blank=True, null=True)
    threshold_value = models.FloatField(blank=True, null=True)
    current_value = models.FloatField(blank=True, null=True)
    alert_status = models.BooleanField(default=False, blank=True, null=True)

    def set_kri(self, indicator_name, threshold_value, current_value):
        self.indicator_name = indicator_name
        self.threshold_value = threshold_value
        self.current_value = current_value
        self.alert_status = False
        self.save()

    def monitor_kri(self):
        if self.current_value >= self.threshold_value:
            self.trigger_alert()

    def trigger_alert(self):
        self.alert_status = True
        self.save()

    def get_kri(self):
        return {
            "id": self.id,
            "indicator_name": self.indicator_name,
            "threshold_value": self.threshold_value,
            "current_value": self.current_value,
            "alert_status": self.alert_status,
        }

class RiskScenario(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    risk_assessment = models.ForeignKey(RiskAssessment, on_delete=models.CASCADE)
    scenario_name = models.CharField(max_length=255, blank=True, null=True)
    scenario_description = models.TextField(blank=True, null=True)
    financial_impact = models.FloatField(blank=True, null=True)
    operational_impact = models.FloatField(blank=True, null=True)
    reputational_impact = models.FloatField(blank=True, null=True)

    def create_scenario(self, name, description, financial_impact, operational_impact, reputational_impact):
        self.scenario_name = name
        self.scenario_description = description
        self.financial_impact = financial_impact
        self.operational_impact = operational_impact
        self.reputational_impact = reputational_impact
        self.save()

    def simulate_scenario(self):
        return {
            "scenario_name": self.scenario_name,
            "financial_impact": self.financial_impact,
            "operational_impact": self.operational_impact,
            "reputational_impact": self.reputational_impact,
        }

    def evaluate_impact(self):
        total_impact = self.financial_impact + self.operational_impact + self.reputational_impact
        return total_impact

    def get_scenario(self):
        return {
            "id": self.id,
            "scenario_name": self.scenario_name,
            "scenario_description": self.scenario_description,
            "financial_impact": self.financial_impact,
            "operational_impact": self.operational_impact,
            "reputational_impact": self.reputational_impact,
        }

class RiskAssessmentReport(Report):
    risk_assessment = models.ForeignKey(RiskAssessment, on_delete=models.CASCADE)
    report_date = models.DateField(auto_now_add=True, blank=True, null=True)
    report_summary = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)

    def generate_report(self):
        title = self.title
        report_summary = self.report_summary
        self.report_summary = f"Report title: {title}. /n Risk Assessment Summary: {report_summary}"
        self.save()

    def customize_report(self, report_summary, recommendations):
        self.report_summary = report_summary
        self.recommendations = recommendations
        self.save()

    def get_report(self):
        return {
            "id": self.report_id,
            "risk_assessment": self.risk_assessment.get_assessment_data(),
            "report_date": self.report_date,
            "report_summary": self.report_summary,
            "recommendations": self.recommendations,
        }

