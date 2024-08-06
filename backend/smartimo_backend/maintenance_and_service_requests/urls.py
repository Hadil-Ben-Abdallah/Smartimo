from django.urls import path
from ninja import NinjaAPI
from maintenance_and_service_requests.views import router

api = NinjaAPI(urls_namespace='maintenance-and-service-requests', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]