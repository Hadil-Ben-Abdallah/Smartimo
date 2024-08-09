from django.urls import path
from ninja import NinjaAPI
from marketing_tools_integration.views import router

api = NinjaAPI(urls_namespace='marketing-tools-integration', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]