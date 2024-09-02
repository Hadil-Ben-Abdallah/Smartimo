from django.db import models
from django.utils import timezone
from core.models import Property, TimeStampedModel

class Meter(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    meter_type = models.CharField(max_length=100, blank=True, null=True)
    installation_date = models.DateField(blank=True, null=True)

    def get_meter_details(self):
        return {
            "id": self.id,
            "property_id": self.property.property_id,
            "meter_type": self.meter_type,
            "installation_date": self.installation_date,
        }

class EnergyConsumptionData(TimeStampedModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    energy_type = models.CharField(max_length=100, choices=[('electricity', 'electricity'), ('gas', 'Gas'), ('water', 'Water'), ('other', 'Other')], default='electricity')
    consumption_value = models.FloatField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def get_data(self, start_date=None, end_date=None):
        data = EnergyConsumptionData.objects.filter(meter=self.meter.id)
        if start_date and end_date:
            data = data.filter(consumption_date__range=[start_date, end_date])
        return data

    def aggregate_data(self, start_date=None, end_date=None):
        data = self.get_data(start_date, end_date)
        aggregated_data = data.aggregate(
            total_consumption=models.Sum('consumption_value'),
            total_cost=models.Sum('cost')
        )
        return aggregated_data

class EnergyConsumptionAnalysis(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    analysis_date = models.DateField(default=timezone.now, blank=True, null=True)
    energy_savings_potential = models.FloatField(blank=True, null=True)
    identified_issues = models.TextField(blank=True, null=True)
    recommended_actions = models.TextField(blank=True, null=True)

    def analyze_patterns(self):
        data = EnergyConsumptionData.objects.filter(property=self.property.property_id)
        issues = []
        potential_savings = 0.0

        for record in data:
            if record.consumption_value > 1000:
                issues.append(f"High consumption detected: {record.energy_type}")
                potential_savings += record.consumption_value * 0.1

        self.identified_issues = "; ".join(issues)
        self.energy_savings_potential = potential_savings

        return {
            "identified_issues": self.identified_issues,
            "energy_savings_potential": self.energy_savings_potential,
        }

    def generate_insights(self):
        insights = {
            "issues": self.identified_issues,
            "recommended_actions": self.recommended_actions,
        }
        return insights

class BenchmarkingTool(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    benchmark_date = models.DateField(default=timezone.now, blank=True, null=True)
    energy_intensity = models.FloatField(blank=True, null=True)
    industry_standard = models.FloatField(blank=True, null=True)
    comparison_result = models.CharField(max_length=100, blank=True, null=True)

    def compare_performance(self):
        if self.energy_intensity > self.industry_standard:
            self.comparison_result = "Below Industry Standard"
        else:
            self.comparison_result = "Above Industry Standard"
        return self.comparison_result

    def generate_benchmark_report(self):
        report = {
            "property_id": self.property.property_id,
            "benchmark_date": self.benchmark_date,
            "energy_intensity": self.energy_intensity,
            "industry_standard": self.industry_standard,
            "comparison_result": self.comparison_result,
        }
        return report

class EnergyEfficiencyInitiative(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    initiative_name = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(null=True, blank=True)
    expected_savings = models.FloatField(blank=True, null=True)
    actual_savings = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=100, blank=True, null=True)

    def track_progress(self):
        progress = {
            "initiative_name": self.initiative_name,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
        return progress

    def evaluate_impact(self):
        if self.end_date:
            duration = (self.end_date - self.start_date).days
        else:
            duration = (timezone.now().date() - self.start_date).days
        
        impact = {
            "expected_savings": self.expected_savings,
            "actual_savings": self.actual_savings,
            "duration": duration,
        }
        return impact

