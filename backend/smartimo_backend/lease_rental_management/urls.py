from django.urls import path
from ninja import NinjaAPI
from lease_rental_management.views import router

api = NinjaAPI(urls_namespace='lease-rental-management', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]