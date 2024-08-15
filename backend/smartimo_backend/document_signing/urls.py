from django.urls import path
from ninja import NinjaAPI
from document_signing.views import router

api = NinjaAPI(urls_namespace='document-signing', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]