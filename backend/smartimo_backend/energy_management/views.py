from ninja import Router
from .models import *
from .schemas import *

router = Router()

@router.get("/devices/", response=List[EnergyMonitoringDeviceSchema])
def list_devices(request):
    return EnergyMonitoringDevice.objects.all()

@router.post("/devices/", response=EnergyMonitoringDeviceSchema)
def create_device(request, payload: EnergyMonitoringDeviceSchema):
    device = EnergyMonitoringDevice.objects.create(**payload.dict(exclude={'id'}))
    return device

@router.get("/dashboards/", response=List[EnergyDashboardSchema])
def list_dashboards(request):
    return EnergyDashboard.objects.all()

@router.post("/dashboards/", response=EnergyDashboardSchema)
def create_dashboard(request, payload: EnergyDashboardSchema):
    dashboard = EnergyDashboard.objects.create(**payload.dict(exclude={'id'}))
    return dashboard

@router.get("/goals/", response=List[EnergyGoalSchema])
def list_goals(request):
    return EnergyGoal.objects.all()

@router.post("/goals/", response=EnergyGoalSchema)
def create_goal(request, payload: EnergyGoalSchema):
    goal = EnergyGoal.objects.create(**payload.dict(exclude={'id'}))
    return goal

@router.get("/recommendations/", response=List[EnergyRecommendationSchema])
def list_recommendations(request):
    return EnergyRecommendation.objects.all()

@router.post("/recommendations/", response=EnergyRecommendationSchema)
def create_recommendation(request, payload: EnergyRecommendationSchema):
    recommendation = EnergyRecommendation.objects.create(**payload.dict(exclude={'id'}))
    return recommendation

@router.get("/tools/", response=List[EnergyModelingToolSchema])
def list_tools(request):
    return EnergyModelingTool.objects.all()

@router.post("/tools/", response=EnergyModelingToolSchema)
def create_tool(request, payload: EnergyModelingToolSchema):
    tool = EnergyModelingTool.objects.create(**payload.dict(exclude={'id'}))
    return tool

@router.get("/audits/", response=List[EnergyAuditSchema])
def list_audits(request):
    return EnergyAudit.objects.all()

@router.post("/audits/", response=EnergyAuditSchema)
def create_audit(request, payload: EnergyAuditSchema):
    audit = EnergyAudit.objects.create(**payload.dict(exclude={'id'}))
    return audit

@router.get("/projects/", response=List[EnergyProjectSchema])
def list_projects(request):
    return EnergyProject.objects.all()

@router.post("/projects/", response=EnergyProjectSchema)
def create_project(request, payload: EnergyProjectSchema):
    project = EnergyProject.objects.create(**payload.dict(exclude={'id'}))
    return project
