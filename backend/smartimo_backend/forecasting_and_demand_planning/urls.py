from django.urls import path
from ninja import NinjaAPI
from forecasting_and_demand_planning.views import router

api = NinjaAPI(urls_namespace='forecasting-and-demand-planning', docs_url='docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]