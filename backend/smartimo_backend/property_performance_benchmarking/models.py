from django.db import models
from core.models import Property
from lease_rental_management.models import PropertyManager

class PropertyBenchmarkingTool(models.Model):
    id = models.AutoField(primary_key=True)
    kpi = models.CharField(max_length=100, blank=True, null=True)
    benchmark_value = models.FloatField(blank=True, null=True)

    def compare_to_industry_standard(self, property_kpi):
        if property_kpi > self.benchmark_value:
            return f"{self.kpi} is above industry standard."
        elif property_kpi < self.benchmark_value:
            return f"{self.kpi} is below industry standard."
        else:
            return f"{self.kpi} is at the industry standard."

    def update_benchmark(self, new_value):
        self.benchmark_value = new_value
        self.save()


class PerformanceDashboard(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    kpi_comparisons = models.JSONField(default=dict, blank=True, null=True)

    def generate_dashboard(self, property_id):
        property = Property.objects.get(id=property_id)
        benchmarks = PropertyBenchmarkingTool.objects.all()
        comparisons = {}
        for benchmark in benchmarks:
            property_kpi = getattr(property, benchmark.kpi, None)
            if property_kpi is not None:
                comparison = benchmark.compare_to_industry_standard(property_kpi)
                comparisons[benchmark.kpi] = comparison
        self.kpi_comparisons = comparisons
        self.save()

    def update_dashboard(self):
        self.generate_dashboard(self.property.property_id)


class Recommendation(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    recommendation_text = models.TextField(blank=True, null=True)

    def generate_recommendations(self, property_id):
        dashboard = PerformanceDashboard.objects.get(property=property_id)
        recommendations = []

        for kpi, comparison in dashboard.kpi_comparisons.items():
            if "below" in comparison:
                recommendations.append(f"Improve {kpi} by enhancing related strategies.")
            elif "above" in comparison:
                recommendations.append(f"Maintain high performance in {kpi}.")

        self.recommendation_text = " | ".join(recommendations)
        self.save()

    def update_recommendations(self):
        self.generate_recommendations(self.property.property_id)


class InvestmentAnalysis(models.Model):
    id = models.OneToOneField(Property, on_delete=models.CASCADE, primary_key=True)
    comparison_metrics = models.JSONField(default=dict, blank=True, null=True)
    financial_projections = models.JSONField(default=dict, blank=True, null=True)

    def perform_analysis(self, property_id):
        property = Property.objects.get(id=property_id)
        benchmarks = PropertyBenchmarkingTool.objects.all()
        metrics = {}

        for benchmark in benchmarks:
            property_kpi = getattr(property, benchmark.kpi, None)
            if property_kpi is not None:
                metrics[benchmark.kpi] = benchmark.compare_to_industry_standard(property_kpi)

        self.comparison_metrics = metrics
        self.save()

    def generate_report(self):
        return {
            "comparison_metrics": self.comparison_metrics,
            "financial_projections": self.financial_projections,
        }


class PropertyCollaboration(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ManyToManyField(PropertyManager)
    benchmarking_project = models.CharField(max_length=255, blank=True, null=True)
    shared_insights = models.JSONField(default=dict, blank=True, null=True)

    def share_insight(self, team_id, insight):
        team = PropertyManager.objects.get(id=team_id)
        if team not in self.team.all():
            self.team.add(team)
        self.shared_insights[str(team_id)] = insight
        self.save()

    def start_collaboration(self, project_name):
        self.benchmarking_project = project_name
        self.save()

