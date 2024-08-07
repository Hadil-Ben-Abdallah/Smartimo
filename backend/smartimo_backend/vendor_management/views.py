from ninja import Router
from .models import Vendor, VendorsPropertyManager, Contract, PerformanceMetrics, VendorsCommunication
from .schemas import VendorSchema, VendorsPropertyManagerSchema, ContractSchema, PerformanceMetricsSchema, VendorsCommunicationSchema

router = Router()

@router.post("/vendors/", response=VendorSchema)
def create_vendor(request, payload: VendorSchema):
    vendor = Vendor.objects.create(**payload.dict(exclude={'id'}))
    return vendor

@router.put("/vendors/{vendor_id}/", response=VendorSchema)
def update_vendor(request, vendor_id: int, payload: VendorSchema):
    vendor = Vendor.objects.get(id=vendor_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(vendor, key, value)
    vendor.save()
    return vendor

@router.post("/property-managers/", response=VendorsPropertyManagerSchema)
def create_property_manager(request, payload: VendorsPropertyManagerSchema):
    property_manager = VendorsPropertyManager.objects.create(**payload.dict(exclude={'id'}))
    return property_manager

@router.put("/property-managers/{property_manager_id}/", response=VendorsPropertyManagerSchema)
def update_property_manager(request, property_manager_id: int, payload: VendorsPropertyManagerSchema):
    property_manager = VendorsPropertyManager.objects.get(id=property_manager_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(property_manager, key, value)
    property_manager.save()
    return property_manager

@router.post("/contracts/", response=ContractSchema)
def create_contract(request, payload: ContractSchema):
    contract = Contract.objects.create(**payload.dict(exclude={'id'}))
    return contract

@router.put("/contracts/{contract_id}/", response=ContractSchema)
def update_contract(request, contract_id: int, payload: ContractSchema):
    contract = Contract.objects.get(id=contract_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(contract, key, value)
    contract.save()
    return contract

@router.post("/performance-metrics/", response=PerformanceMetricsSchema)
def create_performance_metrics(request, payload: PerformanceMetricsSchema):
    metrics = PerformanceMetrics.objects.create(**payload.dict(exclude={'id'}))
    return metrics

@router.put("/performance-metrics/{metrics_id}/", response=PerformanceMetricsSchema)
def update_performance_metrics(request, metrics_id: int, payload: PerformanceMetricsSchema):
    metrics = PerformanceMetrics.objects.get(id=metrics_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(metrics, key, value)
    metrics.save()
    return metrics

@router.post("/vendors-communications/", response=VendorsCommunicationSchema)
def create_communication(request, payload: VendorsCommunicationSchema):
    communication = VendorsCommunication.objects.create(**payload.dict(exclude={'id'}))
    return communication

@router.put("/vendors-communications/{communication_id}/", response=VendorsCommunicationSchema)
def update_communication(request, communication_id: int, payload: VendorsCommunicationSchema):
    communication = VendorsCommunication.objects.get(id=communication_id)
    for key, value in payload.dict().items():
        if key != 'id':
            setattr(communication, key, value)
    communication.save()
    return communication

