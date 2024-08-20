from django.urls import path
from ninja import NinjaAPI
from customizable_reporting_for_tailored_insights.views import router

api = NinjaAPI(urls_namespace='customizable-reporting-for-tailored-insights', docs_url='docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]