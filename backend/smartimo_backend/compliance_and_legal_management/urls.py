from django.urls import path
from ninja import NinjaAPI
from compliance_and_legal_management.views import router

api = NinjaAPI(urls_namespace='compliance-and-legal-management', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]