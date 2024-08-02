from django.urls import path
from ninja import NinjaAPI
from communication_tools.views import router

api = NinjaAPI(urls_namespace='communication-tools', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]