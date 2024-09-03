from django.db import models
from core.models import Property, User, TimeStampedModel
from property_listing.models import PropertyOwner
from remote_property_monitoring.models import Project
from client_management.models import Client
from property_listing.models import RealEstateAgent
from tenant_screening_and_background_checks.models import PropertyManagementCompany

class VirtualTour(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tour_content = models.JSONField(blank=True, null=True)
    branding_options = models.JSONField(blank=True, null=True)
    navigation_controls = models.JSONField(blank=True, null=True)
    hotspots = models.JSONField(blank=True, null=True)
    annotations = models.JSONField(blank=True, null=True)

    def create_tour(self, property_id, tour_content, branding_options, navigation_controls, hotspots, annotations):
        return VirtualTour.objects.create(
            property=property_id,
            tour_content=tour_content,
            branding_options=branding_options,
            navigation_controls=navigation_controls,
            hotspots=hotspots,
            annotations=annotations
        )

    def update_tour(self, tour_id, tour_content):
        tour_instance = VirtualTour.objects.get(id=tour_id)
        tour_instance.tour_content = tour_content
        tour_instance.save()
        return tour_instance

    def embed_tour(self, tour_id, target):
        tour_instance = VirtualTour.objects.get(id=tour_id)
        return f"Virtual tour {tour_id} embedded into {target}"
    
    
class VirtualProperty(Property):
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    floor_plans = models.JSONField(blank=True, null=True)
    amenities = models.JSONField(blank=True, null=True)
    virtual_tours = models.ManyToManyField(VirtualTour, related_name='properties')

    def add_property(self, owner_id, address, description, floor_plans, amenities):
        property_instance, created = Property.objects.get_or_create(
            address=address,
            defaults={'description': description}
        )
        self.owner.user_id= owner_id
        self.floor_plans = floor_plans
        self.amenities = amenities
        self.save()
        return property_instance

    def update_property(self, property_id, description):
        property_instance = Property.objects.get(id=property_id)
        property_instance.description = description
        property_instance.save()
        return property_instance

    def associate_virtual_tour(self, property_id, tour_id):
        property_instance = VirtualProperty.objects.get(id=property_id)
        tour_instance = VirtualTour.objects.get(id=tour_id)
        property_instance.virtual_tours.add(tour_instance)
        property_instance.save()

class ProspectiveClient(Client):
    shortlisted_properties = models.ManyToManyField(VirtualProperty, related_name='shortlisted_by')

    def explore_virtual_tour(self, tour_id):
        tour_instance = VirtualTour.objects.get(id=tour_id)
        return tour_instance

    def shortlist_property(self, client_id, property_id):
        client_instance = ProspectiveClient.objects.get(id=client_id)
        property_instance = VirtualProperty.objects.get(id=property_id)
        client_instance.shortlisted_properties.add(property_instance)
        return property_instance


class LiveVirtualTourSession(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    agent = models.ForeignKey(RealEstateAgent, on_delete=models.CASCADE)
    client = models.ForeignKey(ProspectiveClient, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    agenda = models.TextField(blank=True, null=True)
    tour_route = models.JSONField(blank=True, null=True)

    def schedule_session(self, property_id, agent_id, client_id, scheduled_time, duration, agenda, tour_route):
        return LiveVirtualTourSession.objects.create(
            property=property_id,
            agent=agent_id,
            client=client_id,
            scheduled_time=scheduled_time,
            duration=duration,
            agenda=agenda,
            tour_route=tour_route
        )

    def conduct_tour(self, session_id):
        session_instance = LiveVirtualTourSession.objects.get(id=session_id)
        return f"Conducting live virtual tour session {session_id}"

    def record_session(self, session_id):
        session_instance = LiveVirtualTourSession.objects.get(id=session_id)
        return f"Recording live virtual tour session {session_id}"

class PropertyDeveloper(User):
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    properties = models.ManyToManyField(Property, related_name='developers')
    projects = models.ManyToManyField(Project, related_name='developers')

    def create_property(self, address, description, floor_plans, amenities):
        property_instance = VirtualProperty(
            address=address,
            description=description,
            floor_plans=floor_plans,
            amenities=amenities
        )
        property_instance.save()
        return property_instance

    def manage_project(self, project_id):
        project_instance = Project.objects.get(id=project_id)
        return project_instance

    def view_properties(self):
        return self.properties.all()

    def view_projects(self):
        return self.projects.all()

    def generate_reports(self):
        pass

    def update_contact_info(self, company_name=None, company_address=None):
        if company_name:
            self.company_name = company_name
        if company_address:
            self.company_address = company_address
        self.save()
        return self

class VirtualMarketingCampaign(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    developer = models.ForeignKey(PropertyDeveloper, on_delete=models.CASCADE)
    campaign_name = models.CharField(max_length=255, blank=True, null=True)
    virtual_tours = models.ManyToManyField(VirtualTour, related_name='campaigns')
    embedding_options = models.JSONField(blank=True, null=True)
    sharing_options = models.JSONField(blank=True, null=True)
    analytics = models.JSONField(blank=True, null=True)

    def create_campaign(self, developer_id, campaign_name, virtual_tours, embedding_options, sharing_options):
        return VirtualMarketingCampaign.objects.create(
            developer_id=developer_id,
            campaign_name=campaign_name,
            virtual_tours=virtual_tours,
            embedding_options=embedding_options,
            sharing_options=sharing_options
        )

    def track_engagement(self, campaign_id):
        campaign_instance = VirtualMarketingCampaign.objects.get(id=campaign_id)
        return campaign_instance.analytics

    def optimize_campaign(self, campaign_id, analytics):
        campaign_instance = VirtualMarketingCampaign.objects.get(id=campaign_id)
        campaign_instance.analytics = analytics
        campaign_instance.save()
        return campaign_instance

class VirtualTourServicePackage(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(PropertyManagementCompany, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=255, blank=True, null=True)
    virtual_tour_tools = models.JSONField(blank=True, null=True)
    branding_customization = models.JSONField(blank=True, null=True)
    pricing_options = models.JSONField(blank=True, null=True)
    support_resources = models.JSONField(blank=True, null=True)

    def create_service_package(self, company_id, package_name, virtual_tour_tools, branding_customization, pricing_options, support_resources):
        return VirtualTourServicePackage.objects.create(
            company=company_id,
            package_name=package_name,
            virtual_tour_tools=virtual_tour_tools,
            branding_customization=branding_customization,
            pricing_options=pricing_options,
            support_resources=support_resources
        )

    def update_service_package(self, package_id, virtual_tour_tools):
        package_instance = VirtualTourServicePackage.objects.get(id=package_id)
        package_instance.virtual_tour_tools = virtual_tour_tools
        package_instance.save()
        return package_instance

    def offer_service_package(self, package_id, clients):
        package_instance = VirtualTourServicePackage.objects.get(id=package_id)
        return f"Offering service package {package_id} to clients"

