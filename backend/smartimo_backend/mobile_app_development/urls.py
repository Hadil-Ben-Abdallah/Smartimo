from django.urls import path
from ninja import NinjaAPI
from mobile_app_development.views import router

api = NinjaAPI(urls_namespace='mobile-app-development', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]