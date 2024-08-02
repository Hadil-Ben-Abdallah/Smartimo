from django.urls import path
from ninja import NinjaAPI
from document_management.views import router

api = NinjaAPI(urls_namespace='document-management', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]