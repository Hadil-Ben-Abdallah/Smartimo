from django.urls import path
from ninja import NinjaAPI
from predictive_analytics_for_market_insights.views import router

api = NinjaAPI(urls_namespace='predictive-analytics-for-market-insights', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]