from django.urls import path
from ninja import NinjaAPI
from owner_portal_development.views import router

api = NinjaAPI(urls_namespace='owner-portal-development', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]