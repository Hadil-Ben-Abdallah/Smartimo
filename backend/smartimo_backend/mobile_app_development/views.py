from ninja import Router
from .models import MobileApp, AppProperty, CommunicationManager, TaskManager, NotificationManager, MobileUserAccount
from .schemas import (
    MobileAppSchema, AppPropertySchema, CommunicationManagerSchema, 
    TaskManagerSchema, NotificationManagerSchema, MobileUserAccountSchema
)

router = Router()

@router.post("/mobileapp/", response=MobileAppSchema)
def create_mobile_app(request, payload: MobileAppSchema):
    mobile_app = MobileApp.objects.create(**payload.dict(exclude={'id'}))
    return mobile_app

@router.get("/mobileapp/{app_id}", response=MobileAppSchema)
def get_mobile_app(request, app_id: int):
    mobile_app = MobileApp.objects.get(id=app_id)
    return mobile_app

@router.post("/appproperty/", response=AppPropertySchema)
def create_app_property(request, payload: AppPropertySchema):
    app_property = AppProperty.objects.create(**payload.dict(exclude={'id'}))
    return app_property

@router.get("/appproperty/{property_id}", response=AppPropertySchema)
def get_app_property(request, property_id: int):
    app_property = AppProperty.objects.get(id=property_id)
    return app_property

@router.post("/communicationmanager/", response=CommunicationManagerSchema)
def create_communication_manager(request, payload: CommunicationManagerSchema):
    communication_manager = CommunicationManager.objects.create(**payload.dict(exclude={'id'}))
    return communication_manager

@router.get("/communicationmanager/{comm_id}", response=CommunicationManagerSchema)
def get_communication_manager(request, comm_id: int):
    communication_manager = CommunicationManager.objects.get(id=comm_id)
    return communication_manager

@router.post("/taskmanager/", response=TaskManagerSchema)
def create_task_manager(request, payload: TaskManagerSchema):
    task_manager = TaskManager.objects.create(**payload.dict(exclude={'id'}))
    return task_manager

@router.get("/taskmanager/{task_id}", response=TaskManagerSchema)
def get_task_manager(request, task_id: int):
    task_manager = TaskManager.objects.get(id=task_id)
    return task_manager

@router.post("/notificationmanager/", response=NotificationManagerSchema)
def create_notification_manager(request, payload: NotificationManagerSchema):
    notification_manager = NotificationManager.objects.create(**payload.dict(exclude={'id'}))
    return notification_manager

@router.get("/notificationmanager/{notif_id}", response=NotificationManagerSchema)
def get_notification_manager(request, notif_id: int):
    notification_manager = NotificationManager.objects.get(id=notif_id)
    return notification_manager

@router.post("/mobileuseraccount/", response=MobileUserAccountSchema)
def create_mobile_user_account(request, payload: MobileUserAccountSchema):
    mobile_user_account = MobileUserAccount.objects.create(**payload.dict(exclude={'id'}))
    return mobile_user_account

@router.get("/mobileuseraccount/{user_id}", response=MobileUserAccountSchema)
def get_mobile_user_account(request, user_id: int):
    mobile_user_account = MobileUserAccount.objects.get(id=user_id)
    return mobile_user_account

