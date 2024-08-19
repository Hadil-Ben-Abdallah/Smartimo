from django.urls import path
from ninja import NinjaAPI
from remote_property_monitoring.views import router

api = NinjaAPI(urls_namespace='remote-property-monitoring', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]