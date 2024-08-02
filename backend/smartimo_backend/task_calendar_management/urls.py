from django.urls import path
from ninja import NinjaAPI
from task_calendar_management.views import router

api = NinjaAPI(urls_namespace='task-calendar-management', docs_url='/docs')
api.add_router("/", router)

urlpatterns = [
    path("", api.urls),
]