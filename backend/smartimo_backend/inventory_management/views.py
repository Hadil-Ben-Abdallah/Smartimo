from ninja import Router
from typing import List
from .models import InventoryProperty, InventoryItem, MaintenanceLog, DepreciationRecord, InventoryNotification
from .schemas import (
    InventoryPropertySchema, InventoryItemSchema,
    MaintenanceLogSchema, DepreciationRecordSchema,
    InventoryNotificationSchema
)

router = Router()

@router.get("/inventory-properties", response=List[InventoryPropertySchema])
def list_inventory_properties(request):
    properties = InventoryProperty.objects.all()
    return properties

@router.post("/inventory-properties", response=InventoryPropertySchema)
def create_inventory_property(request, data: InventoryPropertySchema):
    property_data = data.dict(exclude={'id', 'inventory_list'})
    inventory_property = InventoryProperty.objects.create(**property_data)
    return inventory_property

@router.get("/inventory-items", response=List[InventoryItemSchema])
def list_inventory_items(request):
    items = InventoryItem.objects.all()
    return items

@router.post("/inventory-items", response=InventoryItemSchema)
def create_inventory_item(request, data: InventoryItemSchema):
    item_data = data.dict(exclude={'item_id'})
    inventory_item = InventoryItem.objects.create(**item_data)
    return inventory_item

@router.get("/maintenance-logs", response=List[MaintenanceLogSchema])
def list_maintenance_logs(request):
    logs = MaintenanceLog.objects.all()
    return logs

@router.post("/maintenance-logs", response=MaintenanceLogSchema)
def create_maintenance_log(request, data: MaintenanceLogSchema):
    log_data = data.dict(exclude={'log_id'})
    maintenance_log = MaintenanceLog.objects.create(**log_data)
    return maintenance_log

@router.get("/depreciation-records", response=List[DepreciationRecordSchema])
def list_depreciation_records(request):
    records = DepreciationRecord.objects.all()
    return records

@router.post("/depreciation-records", response=DepreciationRecordSchema)
def create_depreciation_record(request, data: DepreciationRecordSchema):
    record_data = data.dict(exclude={'record_id'})
    depreciation_record = DepreciationRecord.objects.create(**record_data)
    return depreciation_record

@router.get("/inventory-notifications", response=List[InventoryNotificationSchema])
def list_inventory_notifications(request):
    notifications = InventoryNotification.objects.all()
    return notifications

@router.post("/inventory-notifications", response=InventoryNotificationSchema)
def create_inventory_notification(request, data: InventoryNotificationSchema):
    notification_data = data.dict(exclude={'id'})
    inventory_notification = InventoryNotification.objects.create(**notification_data)
    return inventory_notification

