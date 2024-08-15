from django.urls import path
from ninja import NinjaAPI
from visitor_management_for_property_access.views import router

api = NinjaAPI(urls_namespace='visitor-management-for-property-access', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]