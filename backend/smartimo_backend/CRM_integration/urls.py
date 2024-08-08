from django.urls import path
from ninja import NinjaAPI
from CRM_integration.views import router

api = NinjaAPI(urls_namespace='CRM-integration', docs_url='docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]