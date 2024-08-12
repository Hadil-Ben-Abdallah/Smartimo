from django.urls import path
from ninja import NinjaAPI
from tenant_portal_development.views import router

api = NinjaAPI(urls_namespace='tenant-portal-development', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]