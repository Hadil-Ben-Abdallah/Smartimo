from django.db import models
from core.models import Property, TimeStampedModel

class CashFlowProjection(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rental_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    operating_expenses = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    financing_terms = models.CharField(max_length=255, blank=True, null=True)
    vacancy_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rental_growth_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    maintenance_costs = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    projection_period = models.IntegerField(blank=True, null=True)
    net_operating_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cash_on_cash_return = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    internal_rate_of_return = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def calculate_cash_flow(self):
        gross_income = self.rental_income * (1 - self.vacancy_rate / 100)
        net_income = gross_income - self.operating_expenses - self.maintenance_costs
        self.net_operating_income = net_income
        self.cash_on_cash_return = (net_income - self.financing_terms) / self.purchase_price * 100
        self.internal_rate_of_return = self._calculate_irr()
        self.save()
        return {
            "net_operating_income": self.net_operating_income,
            "cash_on_cash_return": self.cash_on_cash_return,
            "internal_rate_of_return": self.internal_rate_of_return
        }

    def adjust_parameters(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def generate_reports(self):
        report = {
            "property": self.property.property_id,
            "purchase_price": self.purchase_price,
            "net_operating_income": self.net_operating_income,
            "cash_on_cash_return": self.cash_on_cash_return,
            "internal_rate_of_return": self.internal_rate_of_return
        }
        return report

    def save_projection(self):
        self.save()

    def _calculate_irr(self):
        return self.net_operating_income / self.purchase_price * 100


class ROICalculator(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    financing_costs = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rental_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    operating_expenses = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    resale_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cap_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cash_on_cash_return = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    equity_yield = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def calculate_roi(self):
        self.cap_rate = (self.rental_income - self.operating_expenses) / self.purchase_price * 100
        self.cash_on_cash_return = (self.rental_income - self.financing_costs) / self.purchase_price * 100
        self.equity_yield = (self.resale_value - self.purchase_price) / self.purchase_price * 100
        self.save()
        return {
            "cap_rate": self.cap_rate,
            "cash_on_cash_return": self.cash_on_cash_return,
            "equity_yield": self.equity_yield
        }

    def compare_roi(self, other_properties):
        comparisons = []
        for property in other_properties:
            comparisons.append({
                "property": property.id,
                "cap_rate": property.cap_rate,
                "cash_on_cash_return": property.cash_on_cash_return,
                "equity_yield": property.equity_yield
            })
        return comparisons

    def perform_sensitivity_analysis(self, variable, values):
        results = []
        for value in values:
            setattr(self, variable, value)
            results.append(self.calculate_roi())
        return results

    def save_roi_calculation(self):
        self.save()


class InvestmentRiskAssessment(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    market_risk = models.CharField(max_length=255, blank=True, null=True)
    credit_risk = models.CharField(max_length=255, blank=True, null=True)
    liquidity_risk = models.CharField(max_length=255, blank=True, null=True)
    operational_risk = models.CharField(max_length=255, blank=True, null=True)
    location_risk = models.CharField(max_length=255, blank=True, null=True)
    tenant_risk = models.CharField(max_length=255, blank=True, null=True)
    regulatory_risk = models.CharField(max_length=255, blank=True, null=True)
    macroeconomic_risk = models.CharField(max_length=255, blank=True, null=True)
    risk_profile = models.JSONField(blank=True, null=True)

    def identify_risks(self, **risk_factors):
        for key, value in risk_factors.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def quantify_risks(self):
        self.risk_profile = {
            "market_risk": self.market_risk,
            "credit_risk": self.credit_risk,
            "liquidity_risk": self.liquidity_risk,
            "operational_risk": self.operational_risk,
            "location_risk": self.location_risk,
            "tenant_risk": self.tenant_risk,
            "regulatory_risk": self.regulatory_risk,
            "macroeconomic_risk": self.macroeconomic_risk
        }
        self.save()

    def generate_risk_profile(self):
        risk_profile = {
            "property_id": self.property.property_id,
            "risk_profile": self.risk_profile
        }
        return risk_profile

    def recommend_mitigation_strategies(self):
        strategies = {
            "market_risk": "Diversify portfolio",
            "credit_risk": "Screen tenants thoroughly",
            "liquidity_risk": "Maintain cash reserves",
            "operational_risk": "Regular property inspections",
            "location_risk": "Research local market trends",
            "tenant_risk": "Sign long-term leases",
            "regulatory_risk": "Stay updated on regulations",
            "macroeconomic_risk": "Monitor economic indicators"
        }
        return strategies


class SensitivityAnalysis(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    variables = models.JSONField(blank=True, null=True)
    scenarios = models.JSONField(blank=True, null=True)
    analysis_results = models.JSONField(blank=True, null=True)
    critical_variables = models.JSONField(blank=True, null=True)

    def perform_sensitivity_analysis(self, scenarios):
        results = {}
        for scenario, variables in scenarios.items():
            scenario_result = {}
            for variable, value in variables.items():
                scenario_result[variable] = value
            results[scenario] = scenario_result
        self.analysis_results = results
        self.save()
        return results

    def create_scenarios(self, scenarios):
        self.scenarios = scenarios
        self.save()

    def compare_scenarios(self):
        scenario_comparison = {}
        for scenario, results in self.analysis_results.items():
            scenario_comparison[scenario] = results
        return scenario_comparison

    def save_analysis(self):
        self.save()


class InvestmentPerformanceAnalytics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    total_return = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    capital_appreciation = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    income_yield = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    volatility = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    benchmark_comparison = models.JSONField(blank=True, null=True)
    performance_insights = models.TextField(blank=True, null=True)

    def aggregate_performance_metrics(self):
        self.total_return = self.capital_appreciation + self.income_yield
        self.volatility = (self.total_return - self.capital_appreciation) / self.total_return * 100
        self.save()
        return {
            "total_return": self.total_return,
            "volatility": self.volatility
        }

    def benchmark_against_market(self, benchmark_data):
        self.benchmark_comparison = {
            "market_benchmark": benchmark_data,
            "property_performance": self.total_return
        }
        self.save()

    def generate_performance_reports(self):
        report = {
            "property_id": self.property.property_id,
            "total_return": self.total_return,
            "capital_appreciation": self.capital_appreciation,
            "income_yield": self.income_yield,
            "volatility": self.volatility,
            "benchmark_comparison": self.benchmark_comparison
        }
        return report

    def provide_recommendations(self):
        insights = "Maintain a diversified portfolio and regularly review market conditions."
        return insights

