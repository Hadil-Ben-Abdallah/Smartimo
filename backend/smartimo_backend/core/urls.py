from django.urls import path
from ninja import NinjaAPI
from core.views import router

api = NinjaAPI(urls_namespace='core', docs_url='docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]