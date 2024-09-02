from django.db import models
from datetime import datetime
from core.models import Property, TimeStampedModel
from lease_rental_management.models import PropertyManager
from property_listing.models import PropertyOwner
from property_performance_benchmarking.models import PerformanceDashboard

class PropertyBudget(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_by = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    budget_year = models.IntegerField(blank=True, null=True)
    income_sources = models.JSONField(default=dict, blank=True, null=True)
    expenses = models.JSONField(default=dict)
    capital_expenditures = models.JSONField(default=dict, blank=True, null=True)
    reserve_funds = models.FloatField(default=0.0, blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('draft', 'draft'), ('submitted', 'submitted'), ('approved', 'Approved')],default='draft')

    def create_budget(self, property_id, created_by, budget_year, income_sources, expenses, capital_expenditures, reserve_funds):
        self.property.property_id = property_id
        self.created_by = created_by
        self.budget_year = budget_year
        self.income_sources = income_sources
        self.expenses = expenses
        self.capital_expenditures = capital_expenditures
        self.reserve_funds = reserve_funds
        self.status = 'draft'
        self.save()
        return self

    def edit_budget(self, income_sources=None, expenses=None, capital_expenditures=None, reserve_funds=None):
        if income_sources:
            self.income_sources.update(income_sources)
        if expenses:
            self.expenses.update(expenses)
        if capital_expenditures:
            self.capital_expenditures.update(capital_expenditures)
        if reserve_funds is not None:
            self.reserve_funds = reserve_funds
        self.save()
        return self

    def submit_budget(self):
        self.status = 'submitted'
        self.save()

    def get_budget_details(self):
        return {
            "property": self.property.property_id,
            "created_by": self.created_by,
            "budget_year": self.budget_year,
            "income_sources": self.income_sources,
            "expenses": self.expenses,
            "capital_expenditures": self.capital_expenditures,
            "reserve_funds": self.reserve_funds,
            "status": self.status,
        }

class BudgetApproval(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    budget = models.ForeignKey(PropertyBudget, on_delete=models.CASCADE)
    property_owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    approval_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],default='pending')
    comments = models.TextField(null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)

    def review_budget(self, comments=None):
        if comments:
            self.comments = comments
        self.save()

    def approve_budget(self):
        self.approval_status = 'approved'
        self.approval_date = datetime.now()
        self.save()

    def reject_budget(self, comments):
        self.approval_status = 'rejected'
        self.comments = comments
        self.approval_date = datetime.now()
        self.save()

    def get_approval_status(self):
        return {
            "approval_status": self.approval_status,
            "comments": self.comments,
            "approval_date": self.approval_date,
        }

class BudgetPerformance(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    budget = models.ForeignKey(PropertyBudget, on_delete=models.CASCADE)
    actual_income = models.JSONField(default=dict, blank=True, null=True)
    actual_expenses = models.JSONField(default=dict)
    actual_capital_expenditures = models.JSONField(default=dict, blank=True, null=True)
    variance_analysis = models.JSONField(default=dict, blank=True, null=True)

    def generate_performance_report(self):
        budget = self.budget.id
        self.variance_analysis = {
            "income_variance": {
                source: self.actual_income.get(source, 0) - self.budget.income_sources.get(source, 0)
                for source in self.budget.income_sources
            },
            "expense_variance": {
                expense: self.actual_expenses.get(expense, 0) - self.budget.expenses.get(expense, 0)
                for expense in self.budget.expenses
            },
            "capital_expenditure_variance": {
                expenditure: self.actual_capital_expenditures.get(expenditure, 0) - self.budget.capital_expenditures.get(expenditure, 0)
                for expenditure in self.budget.capital_expenditures
            }
        }
        self.save()
        return self.variance_analysis

    def analyze_variances(self):
        analysis = {
            "income_analysis": {
                source: "Over budget" if variance > 0 else "Under budget"
                for source, variance in self.variance_analysis.get("income_variance", {}).items()
            },
            "expense_analysis": {
                expense: "Over budget" if variance > 0 else "Under budget"
                for expense, variance in self.variance_analysis.get("expense_variance", {}).items()
            },
            "capital_expenditure_analysis": {
                expenditure: "Over budget" if variance > 0 else "Under budget"
                for expenditure, variance in self.variance_analysis.get("capital_expenditure_variance", {}).items()
            }
        }
        return analysis

    def get_performance_details(self):
        return {
            "actual_income": self.actual_income,
            "actual_expenses": self.actual_expenses,
            "actual_capital_expenditures": self.actual_capital_expenditures,
            "variance_analysis": self.variance_analysis,
        }

class BudgetInsight(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    budget = models.ForeignKey(PropertyBudget, on_delete=models.CASCADE)
    insight_summary = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)

    def create_insight(self, budget_id, insight_summary, recommendations):
        self.budget = budget_id
        self.insight_summary = insight_summary
        self.recommendations = recommendations
        self.save()
        return self

    def edit_insight(self, insight_summary=None, recommendations=None):
        if insight_summary:
            self.insight_summary = insight_summary
        if recommendations:
            self.recommendations = recommendations
        self.save()
        return self

    def get_insight_details(self):
        return {
            "budget_id": self.budget.id,
            "insight_summary": self.insight_summary,
            "recommendations": self.recommendations,
        }

class PropertyPerformanceDashboard(PerformanceDashboard):
    kpi_metrics = models.JSONField(default=dict, blank=True, null=True)
    roi_metrics = models.JSONField(default=dict, blank=True, null=True)
    performance_trends = models.JSONField(default=dict, blank=True, null=True)

    def get_dashboard_details(self):
        return {
            "property": self.property.property_id,
            "kpi_comparisons": self.kpi_comparisons,
            "kpi_metrics": self.kpi_metrics,
            "roi_metrics": self.roi_metrics,
            "performance_trends": self.performance_trends,
        }

class BudgetingInvestmentAnalysis(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    investment_metrics = models.JSONField(default=dict, blank=True, null=True)
    investment_summary = models.TextField(blank=True, null=True)

    def perform_analysis(self, property_id, investment_metrics, investment_summary):
        self.property = property_id
        self.investment_metrics = investment_metrics
        self.investment_summary = investment_summary
        self.save()
        return self

    def get_investment_summary(self):
        return {
            "property_id": self.property.property_id,
            "investment_metrics": self.investment_metrics,
            "investment_summary": self.investment_summary,
        }

    def update_investment_data(self, investment_metrics=None, investment_summary=None):
        if investment_metrics:
            self.investment_metrics.update(investment_metrics)
        if investment_summary:
            self.investment_summary = investment_summary
        self.save()
        return self

