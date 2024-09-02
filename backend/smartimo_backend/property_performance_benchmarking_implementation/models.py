from django.db import models
from lease_rental_management.models import PropertyManager
from core.models import TimeStampedModel

class KPIFramework(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    kpi_definitions = models.JSONField(default=dict, blank=True, null=True)
    property_type = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    market_segment = models.CharField(max_length=100, blank=True, null=True)
    industry_guidelines = models.TextField(blank=True, null=True)

    def define_kpi(self, kpi_name, kpi_definition):
        self.kpi_definitions[kpi_name] = kpi_definition
        self.save()

    def select_kpi_by_segment(self, segment):
        return {kpi: definition for kpi, definition in self.kpi_definitions.items() if self.market_segment == segment}

    def get_industry_guidelines(self):
        return self.industry_guidelines


class PerformanceDataCollector(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    data_sources = models.JSONField(default=list, blank=True, null=True)
    aggregated_data = models.JSONField(blank=True, null=True)
    real_time_metrics = models.JSONField(blank=True, null=True)
    historical_trends = models.JSONField(blank=True, null=True)

    def collect_data(self, source_name, data):
        if source_name in self.data_sources:
            self.aggregated_data[source_name] = data
            self.save()

    def aggregate_data(self):
        for source, data in self.aggregated_data.items():
            if source not in self.real_time_metrics:
                self.real_time_metrics[source] = []
            self.real_time_metrics[source].append(data)
        self.save()

    def generate_performance_dashboard(self):
        dashboard = {
            "Real-time Metrics": self.real_time_metrics,
            "Historical Trends": self.historical_trends
        }
        return dashboard


class BenchmarkAnalyzer(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    kpi_definitions = models.JSONField(blank=True, null=True)
    industry_benchmarks = models.JSONField(blank=True, null=True)
    competitor_metrics = models.JSONField(blank=True, null=True)
    benchmark_results = models.JSONField(blank=True, null=True)

    def compare_to_benchmarks(self):
        results = {}
        for kpi, definition in self.kpi_definitions.items():
            benchmark = self.industry_benchmarks.get(kpi, None)
            competitor = self.competitor_metrics.get(kpi, None)
            if benchmark and competitor:
                results[kpi] = {
                    "property": definition,
                    "benchmark": benchmark,
                    "competitor": competitor,
                    "comparison": "outperform" if definition > benchmark else "underperform"
                }
        self.benchmark_results = results
        self.save()

    def generate_visualizations(self):
        visualizations = {
            "heatmap": "generated_heatmap_url",
            "scorecards": "generated_scorecards_url"
        }
        return visualizations

    def highlight_performance_outliers(self):
        outliers = {}
        for kpi, result in self.benchmark_results.items():
            if result["comparison"] == "underperform":
                outliers[kpi] = result
        return outliers


class AnomalyDetector(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    performance_data = models.JSONField(blank=True, null=True)
    anomaly_thresholds = models.JSONField(blank=True, null=True)
    alerts = models.JSONField(default=dict, blank=True, null=True)
    investigation_tools = models.JSONField(blank=True, null=True)

    def detect_anomalies(self):
        for kpi, data in self.performance_data.items():
            threshold = self.anomaly_thresholds.get(kpi, None)
            if threshold and data > threshold:
                self.alerts[kpi] = f"Anomaly detected: {data} exceeds threshold {threshold}"
        self.save()

    def send_alerts(self):
        return self.alerts

    def investigate_anomalies(self, kpi):
        tools = self.investigation_tools.get(kpi, [])
        investigation = {
            "kpi": kpi,
            "tools": tools,
            "action": "Contact maintenance team for review"
        }
        return investigation


class PerformanceMonitor(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    historical_performance_data = models.JSONField(blank=True, null=True)
    current_metrics = models.JSONField(blank=True, null=True)
    trend_reports = models.JSONField(blank=True, null=True)

    def track_performance(self):
        performance_changes = {}
        for kpi, current in self.current_metrics.items():
            historical = self.historical_performance_data.get(kpi, [])
            if historical:
                change = current - historical[-1]
                performance_changes[kpi] = change
        return performance_changes

    def compare_to_historical_benchmarks(self):
        comparisons = {}
        for kpi, current in self.current_metrics.items():
            historical = self.historical_performance_data.get(kpi, [])
            if historical:
                benchmark = sum(historical) / len(historical)
                comparisons[kpi] = {
                    "current": current,
                    "benchmark": benchmark,
                    "comparison": "improved" if current > benchmark else "declined"
                }
        return comparisons

    def generate_trend_reports(self):
        trend_reports = {
            "occupancy_trend": "occupancy_trend_chart_url",
            "revenue_growth": "revenue_growth_chart_url"
        }
        return trend_reports

