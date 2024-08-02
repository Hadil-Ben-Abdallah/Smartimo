from django.urls import path
from ninja import NinjaAPI
from property_listing.views import router

api = NinjaAPI(urls_namespace='property-listing', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]



