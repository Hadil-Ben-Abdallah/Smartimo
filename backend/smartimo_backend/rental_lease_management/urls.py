from django.urls import path
from ninja import NinjaAPI
from rental_lease_management.views import router

api = NinjaAPI(urls_namespace='rental-lease-management', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]
