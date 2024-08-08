from django.urls import path
from ninja import NinjaAPI
from marketplace_integration.views import router

api = NinjaAPI(urls_namespace='marketplace-integration', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]