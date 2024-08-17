from django.urls import path
from ninja import NinjaAPI
from integration_with_accounting_software.views import router

api = NinjaAPI(urls_namespace='integration-with-accounting-software', docs_url='docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]