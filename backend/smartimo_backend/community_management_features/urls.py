from django.urls import path
from ninja import NinjaAPI
from community_management_features.views import router

api = NinjaAPI(urls_namespace='community-management-features', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]