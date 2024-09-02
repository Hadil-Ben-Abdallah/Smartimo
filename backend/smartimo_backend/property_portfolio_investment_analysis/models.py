from django.db import models
from core.models import Property
from decimal import Decimal
import numpy as np


class PropertyInvestmentAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    financing_terms = models.JSONField(blank=True, null=True)
    operating_expenses = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    rental_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    cash_flows = models.JSONField(blank=True, null=True)
    financial_projections = models.JSONField(null=True, blank=True)
    risk_assessment = models.JSONField(null=True, blank=True)
    roi_metrics = models.JSONField(null=True, blank=True)

    def generate_financial_projections(self):
        years = 10
        cash_flows = []
        for year in range(1, years + 1):
            revenue = self.rental_income * 12
            expenses = self.operating_expenses * 12
            cash_flow = revenue - expenses
            cash_flows.append(cash_flow)
        
        income_statements = {"yearly_cash_flows": cash_flows}
        balance_sheets = {"total_income": sum(cash_flows), "total_expenses": expenses * years}

        self.cash_flows = cash_flows
        self.financial_projections = {"income_statements": income_statements, "balance_sheets": balance_sheets}
        self.save()

    def calculate_roi(self):
        total_cash_flows = sum(self.cash_flows)
        cash_on_cash_return = (total_cash_flows / self.purchase_price) * 100
        
        cap_rate = (self.rental_income * 12) / self.purchase_price
        
        irr = np.irr([-self.purchase_price] + self.cash_flows)

        discount_rate = Decimal('0.05')  # 5% discount rate
        npv = sum([cf / (1 + discount_rate)**i for i, cf in enumerate(self.cash_flows, 1)])

        self.roi_metrics = {
            "cash_on_cash_return": cash_on_cash_return,
            "cap_rate": cap_rate,
            "irr": irr,
            "npv": npv
        }
        self.save()

    def perform_risk_assessment(self):
        market_risk = Decimal('0.15')  # 0.15 risk factor
        liquidity_risk = Decimal('0.10')  # 0.1 risk factor

        sensitivity_analysis = {
            "market_risk_impact": self.purchase_price * market_risk,
            "liquidity_risk_impact": self.purchase_price * liquidity_risk
        }
        
        stress_test = {
            "extreme_scenario": self.purchase_price - (self.purchase_price * (market_risk + liquidity_risk))
        }

        self.risk_assessment = {
            "market_risk": market_risk,
            "liquidity_risk": liquidity_risk,
            "sensitivity_analysis": sensitivity_analysis,
            "stress_test": stress_test
        }
        self.save()

    def integrate_market_data(self, market_data):
        self.financial_projections["market_data"] = market_data
        self.save()

    def generate_reports(self):
        report = {
            "financial_projections": self.financial_projections,
            "roi_metrics": self.roi_metrics,
            "risk_assessment": self.risk_assessment
        }
        return report

    def compare_investments(self, other_analysis):
        comparison = {
            "self_roi": self.roi_metrics,
            "other_roi": other_analysis.roi_metrics
        }
        return comparison

    def visualize_data(self):
        return {
            "yearly_cash_flows": self.financial_projections["income_statements"]["yearly_cash_flows"]
        }

    def collaborate_with_stakeholders(self, workspace):
        report = self.generate_reports()
        workspace.share_documents(report)

class MarketData(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    valuation_data = models.JSONField(blank=True, null=True)
    rental_trends = models.JSONField(blank=True, null=True)
    vacancy_rates = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    economic_indicators = models.JSONField(blank=True, null=True)

    def fetch_market_data(self):
        self.valuation_data = {"current_valuation": 500000}
        self.rental_trends = {"trend": "upward"}
        self.vacancy_rates = Decimal('5.5')
        self.economic_indicators = {"GDP_growth": "2.5%"}
        self.save()

    def analyze_market_trends(self):
        if self.rental_trends.get("trend") == "upward":
            return "Positive Market Outlook"
        else:
            return "Cautious Market Outlook"

    def benchmark_investments(self, benchmarks):
        comparison = {
            "current_valuation_vs_benchmark": self.valuation_data["current_valuation"] / benchmarks["average_valuation"]
        }
        return comparison

    def generate_market_reports(self):
        report = {
            "valuation_data": self.valuation_data,
            "rental_trends": self.rental_trends,
            "vacancy_rates": self.vacancy_rates,
            "economic_indicators": self.economic_indicators
        }
        return report

class AnalysisRiskAssessment(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    risk_factors = models.JSONField(blank=True, null=True)
    risk_indicators = models.JSONField(blank=True, null=True)
    stress_tests = models.JSONField(blank=True, null=True)
    risk_mitigation_strategies = models.JSONField(blank=True, null=True)

    def identify_risks(self):
        self.risk_factors = {"market_risk": "high", "credit_risk": "medium"}
        self.save()

    def perform_sensitivity_analysis(self):
        self.risk_indicators = {"market_risk_sensitivity": 0.15, "credit_risk_sensitivity": 0.10}
        self.save()

    def conduct_stress_tests(self):
        self.stress_tests = {"worst_case_scenario": "30% loss in property value"}
        self.save()

    def recommend_mitigation_strategies(self):
        self.risk_mitigation_strategies = {"diversification": "invest in different regions", "insurance": "obtain property insurance"}
        self.save()

class CollaborativeWorkspace(models.Model):
    id = models.AutoField(primary_key=True)
    analysis = models.ForeignKey(PropertyInvestmentAnalysis, on_delete=models.CASCADE)
    stakeholders = models.JSONField(blank=True, null=True)
    shared_documents = models.JSONField(blank=True, null=True)
    comments = models.JSONField(blank=True, null=True)

    def share_documents(self, document):
        if "documents" not in self.shared_documents:
            self.shared_documents["documents"] = []
        self.shared_documents["documents"].append(document)
        self.save()

    def manage_permissions(self, user, permissions):
        if "permissions" not in self.shared_documents:
            self.shared_documents["permissions"] = {}
        self.shared_documents["permissions"][user] = permissions
        self.save()

    def facilitate_discussions(self, comment):
        if "comments" not in self.comments:
            self.comments["comments"] = []
        self.comments["comments"].append(comment)
        self.save()

    def track_changes(self, change_summary):
        if "changes" not in self.shared_documents:
            self.shared_documents["changes"] = []
        self.shared_documents["changes"].append(change_summary)
        self.save()
