from ninja import Router
from django.shortcuts import get_object_or_404
from .models import (
    PredictiveAnalytics,
    InvestmentDashboard,
    MarketTrendAnalysis,
    RentalDemandForecast,
    PropertyValuationModel,
    DevelopmentFeasibilityTool,
)
from .schemas import (
    PredictiveAnalyticsSchema,
    InvestmentDashboardSchema,
    MarketTrendAnalysisSchema,
    RentalDemandForecastSchema,
    PropertyValuationModelSchema,
    DevelopmentFeasibilityToolSchema,
)

router = Router()

@router.post("/predictive-analytics/", response=PredictiveAnalyticsSchema)
def create_predictive_analytics(request, data: PredictiveAnalyticsSchema):
    analytics = PredictiveAnalytics.objects.create(**data.dict(exclude={'id'}))
    return analytics

@router.put("/predictive-analytics/{predictive_id}/", response=PredictiveAnalyticsSchema)
def update_predictive_analytics(request, predictive_id: int, data: PredictiveAnalyticsSchema):
    analytics = get_object_or_404(PredictiveAnalytics, id=predictive_id)
    for key, value in data.dict().items():
        if key != 'id':
            setattr(analytics, key, value)
    analytics.save()
    return analytics


@router.post("/investment-dashboard/", response=InvestmentDashboardSchema)
def create_investment_dashboard(request, data: InvestmentDashboardSchema):
    dashboard = InvestmentDashboard.objects.create(**data.dict(exclude={'id'}))
    return dashboard

@router.put("/investment-dashboard/{dashboard_id}/", response=InvestmentDashboardSchema)
def update_investment_dashboard(request, dashboard_id: int, data: InvestmentDashboardSchema):
    dashboard = get_object_or_404(InvestmentDashboard, id=dashboard_id)
    for key, value in data.dict().items():
        if key != 'id':
            setattr(dashboard, key, value)
    dashboard.save()
    return dashboard


@router.post("/market-trend-analysis/", response=MarketTrendAnalysisSchema)
def create_market_trend_analysis(request, data: MarketTrendAnalysisSchema):
    analysis = MarketTrendAnalysis.objects.create(**data.dict(exclude={'id'}))
    return analysis

@router.put("/market-trend-analysis/{analysis_id}/", response=MarketTrendAnalysisSchema)
def update_market_trend_analysis(request, analysis_id: int, data: MarketTrendAnalysisSchema):
    analysis = get_object_or_404(MarketTrendAnalysis, id=analysis_id)
    for key, value in data.dict().items():
        if key != 'id':
            setattr(analysis, key, value)
    analysis.save()
    return analysis


@router.post("/rental-demand-forecast/", response=RentalDemandForecastSchema)
def create_rental_demand_forecast(request, data: RentalDemandForecastSchema):
    forecast = RentalDemandForecast.objects.create(**data.dict(exclude={'id'}))
    return forecast

@router.put("/rental-demand-forecast/{forecast_id}/", response=RentalDemandForecastSchema)
def update_rental_demand_forecast(request, forecast_id: int, data: RentalDemandForecastSchema):
    forecast = get_object_or_404(RentalDemandForecast, id=forecast_id)
    for key, value in data.dict().items():
        if key != 'id':
            setattr(forecast, key, value)
    forecast.save()
    return forecast


@router.post("/property-valuation-model/", response=PropertyValuationModelSchema)
def create_property_valuation_model(request, data: PropertyValuationModelSchema):
    valuation = PropertyValuationModel.objects.create(**data.dict(exclude={'id'}))
    return valuation

@router.put("/property-valuation-model/{valuation_id}/", response=PropertyValuationModelSchema)
def update_property_valuation_model(request, valuation_id: int, data: PropertyValuationModelSchema):
    valuation = get_object_or_404(PropertyValuationModel, id=valuation_id)
    for key, value in data.dict().items():
        if key != 'id':
            setattr(valuation, key, value)
    valuation.save()
    return valuation


@router.post("/development-feasibility-tool/", response=DevelopmentFeasibilityToolSchema)
def create_development_feasibility_tool(request, data: DevelopmentFeasibilityToolSchema):
    feasibility = DevelopmentFeasibilityTool.objects.create(**data.dict(exclude={'id'}))
    return feasibility

@router.put("/development-feasibility-tool/{feasibility_id}/", response=DevelopmentFeasibilityToolSchema)
def update_development_feasibility_tool(request, feasibility_id: int, data: DevelopmentFeasibilityToolSchema):
    feasibility = get_object_or_404(DevelopmentFeasibilityTool, id=feasibility_id)
    for key, value in data.dict().items():
        if key != 'id':
            setattr(feasibility, key, value)
    feasibility.save()
    return feasibility

