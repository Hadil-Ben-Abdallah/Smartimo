from django.urls import path
from ninja import NinjaAPI
from inventory_management.views import router

api = NinjaAPI(urls_namespace='inventory-management', docs_url='docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]