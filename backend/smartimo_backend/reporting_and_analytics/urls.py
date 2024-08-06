from django.urls import path
from ninja import NinjaAPI
from reporting_and_analytics.views import router

api = NinjaAPI(urls_namespace='reporting-and-analytics', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]