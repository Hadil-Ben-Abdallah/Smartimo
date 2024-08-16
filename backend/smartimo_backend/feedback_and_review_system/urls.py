from django.urls import path
from ninja import NinjaAPI
from feedback_and_review_system.views import router

api = NinjaAPI(urls_namespace='feedback-and-review-system', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]