from django.urls import path
from ninja import NinjaAPI
from sustainability_tracking.views import router

api = NinjaAPI(urls_namespace='sustainability-tracking', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]