from ninja import Router
from .models import (
    DemandForecast, MarketDemand, DevelopmentFeasibility, CommercialDemand, ClientForecastingService
)
from .schemas import (
    DemandForecastSchema, MarketDemandSchema, DevelopmentFeasibilitySchema,
    CommercialDemandSchema, ClientForecastingServiceSchema
)
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

router = Router()

# Demand Forecast
@router.post('/demand-forecast/', response=DemandForecastSchema)
def create_demand_forecast(request, data: DemandForecastSchema):
    forecast = DemandForecast.objects.create(**data.dict(exclude={'id'}))
    return forecast

@router.get('/demand-forecast/{forecast_id}', response=DemandForecastSchema)
def get_demand_forecast(request, forecast_id: int):
    forecast = get_object_or_404(DemandForecast, forecast_id=forecast_id)
    return forecast

@router.put('/demand-forecast/{forecast_id}', response=DemandForecastSchema)
def update_demand_forecast(request, forecast_id: int, data: DemandForecastSchema):
    forecast = get_object_or_404(DemandForecast, forecast_id=forecast_id)
    for attr, value in data.dict().items():
        if attr != 'id':
            setattr(forecast, attr, value)
    forecast.save()
    return forecast

@router.delete('/demand-forecast/{forecast_id}')
def delete_demand_forecast(request, forecast_id: int):
    forecast = get_object_or_404(DemandForecast, forecast_id=forecast_id)
    forecast.delete()
    return JsonResponse({'success': True})

# Market Demand
@router.post('/market-demand/', response=MarketDemandSchema)
def create_market_demand(request, data: MarketDemandSchema):
    demand = MarketDemand.objects.create(**data.dict(exclude={'id'}))
    return demand

@router.get('/market-demand/{demand_id}', response=MarketDemandSchema)
def get_market_demand(request, demand_id: int):
    demand = get_object_or_404(MarketDemand, demand_id=demand_id)
    return demand

@router.put('/market-demand/{demand_id}', response=MarketDemandSchema)
def update_market_demand(request, demand_id: int, data: MarketDemandSchema):
    demand = get_object_or_404(MarketDemand, demand_id=demand_id)
    for attr, value in data.dict().items():
        if attr != 'id':
            setattr(demand, attr, value)
    demand.save()
    return demand

@router.delete('/market-demand/{demand_id}')
def delete_market_demand(request, demand_id: int):
    demand = get_object_or_404(MarketDemand, demand_id=demand_id)
    demand.delete()
    return JsonResponse({'success': True})

# Development Feasibility
@router.post('/development-feasibility/', response=DevelopmentFeasibilitySchema)
def create_development_feasibility(request, data: DevelopmentFeasibilitySchema):
    feasibility = DevelopmentFeasibility.objects.create(**data.dict(exclude={'id'}))
    return feasibility

@router.get('/development-feasibility/{feasibility_id}', response=DevelopmentFeasibilitySchema)
def get_development_feasibility(request, feasibility_id: int):
    feasibility = get_object_or_404(DevelopmentFeasibility, feasibility_id=feasibility_id)
    return feasibility

@router.put('/development-feasibility/{feasibility_id}', response=DevelopmentFeasibilitySchema)
def update_development_feasibility(request, feasibility_id: int, data: DevelopmentFeasibilitySchema):
    feasibility = get_object_or_404(DevelopmentFeasibility, feasibility_id=feasibility_id)
    for attr, value in data.dict().items():
        if attr != 'id':
            setattr(feasibility, attr, value)
    feasibility.save()
    return feasibility

@router.delete('/development-feasibility/{feasibility_id}')
def delete_development_feasibility(request, feasibility_id: int):
    feasibility = get_object_or_404(DevelopmentFeasibility, feasibility_id=feasibility_id)
    feasibility.delete()
    return JsonResponse({'success': True})

# Commercial Demand
@router.post('/commercial-demand/', response=CommercialDemandSchema)
def create_commercial_demand(request, data: CommercialDemandSchema):
    commercial_demand = CommercialDemand.objects.create(**data.dict(exclude={'id'}))
    return commercial_demand

@router.get('/commercial-demand/{demand_id}', response=CommercialDemandSchema)
def get_commercial_demand(request, demand_id: int):
    commercial_demand = get_object_or_404(CommercialDemand, demand_id=demand_id)
    return commercial_demand

@router.put('/commercial-demand/{demand_id}', response=CommercialDemandSchema)
def update_commercial_demand(request, demand_id: int, data: CommercialDemandSchema):
    commercial_demand = get_object_or_404(CommercialDemand, demand_id=demand_id)
    for attr, value in data.dict().items():
        if attr != 'id':
            setattr(commercial_demand, attr, value)
    commercial_demand.save()
    return commercial_demand

@router.delete('/commercial-demand/{demand_id}')
def delete_commercial_demand(request, demand_id: int):
    commercial_demand = get_object_or_404(CommercialDemand, demand_id=demand_id)
    commercial_demand.delete()
    return JsonResponse({'success': True})

# Client Forecasting Service
@router.post('/client-forecasting-service/', response=ClientForecastingServiceSchema)
def create_client_forecasting_service(request, data: ClientForecastingServiceSchema):
    service = ClientForecastingService.objects.create(**data.dict(exclude={'id'}))
    return service

@router.get('/client-forecasting-service/{service_id}', response=ClientForecastingServiceSchema)
def get_client_forecasting_service(request, service_id: int):
    service = get_object_or_404(ClientForecastingService, service_id=service_id)
    return service

@router.put('/client-forecasting-service/{service_id}', response=ClientForecastingServiceSchema)
def update_client_forecasting_service(request, service_id: int, data: ClientForecastingServiceSchema):
    service = get_object_or_404(ClientForecastingService, service_id=service_id)
    for attr, value in data.dict().items():
        if attr != 'id':
            setattr(service, attr, value)
    service.save()
    return service

@router.delete('/client-forecasting-service/{service_id}')
def delete_client_forecasting_service(request, service_id: int):
    service = get_object_or_404(ClientForecastingService, service_id=service_id)
    service.delete()
    return JsonResponse({'success': True})
