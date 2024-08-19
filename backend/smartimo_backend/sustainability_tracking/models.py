from django.db import models
from core.models import Property, Resource, User
from lease_rental_management.models import Tenant
from django.core.exceptions import ObjectDoesNotExist

class SustainabilityInitiative(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    description = models.TextField()
    implementation_date = models.DateField()
    resource_savings = models.JSONField()
    environmental_impact = models.JSONField()

    def log_initiative(self, property_id, description, implementation_date, resource_savings, environmental_impact):
        property_instance = Property.objects.get(id=property_id)
        initiative = SustainabilityInitiative(
            property=property_instance,
            description=description,
            implementation_date=implementation_date,
            resource_savings=resource_savings,
            environmental_impact=environmental_impact
        )
        initiative.save()
        return initiative

    def update_initiative(self, initiative_id, updates):
        try:
            initiative = SustainabilityInitiative.objects.get(id=initiative_id)
            for attr, value in updates.items():
                setattr(initiative, attr, value)
            initiative.save()
            return initiative
        except ObjectDoesNotExist:
            return None

    def delete_initiative(self, initiative_id):
        try:
            initiative = SustainabilityInitiative.objects.get(id=initiative_id)
            initiative.delete()
            return {"success": True}
        except ObjectDoesNotExist:
            return {"success": False, "error": "Initiative not found"}

    def generate_initiative_report(self, property_id):
        initiatives = SustainabilityInitiative.objects.filter(property_id=property_id)
        report = {
            "property_id": property_id,
            "initiatives": []
        }
        for initiative in initiatives:
            report["initiatives"].append({
                "description": initiative.description,
                "implementation_date": initiative.implementation_date,
                "resource_savings": initiative.resource_savings,
                "environmental_impact": initiative.environmental_impact
            })
        return report

class SustainabilityDashboard(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    energy_consumption = models.JSONField()
    water_usage = models.JSONField()
    waste_generation = models.JSONField()
    ghg_emissions = models.JSONField()

    def visualize_sustainability_data(self, dashboard_id):
        try:
            dashboard = SustainabilityDashboard.objects.get(id=dashboard_id)
            return {
                "energy_consumption": dashboard.energy_consumption,
                "water_usage": dashboard.water_usage,
                "waste_generation": dashboard.waste_generation,
                "ghg_emissions": dashboard.ghg_emissions
            }
        except ObjectDoesNotExist:
            return {"error": "Dashboard not found"}

    def set_targets(self, dashboard_id, targets):
        try:
            dashboard = SustainabilityDashboard.objects.get(id=dashboard_id)
            # Targets is a dictionary with new target values
            dashboard.energy_consumption["target"] = targets.get("energy_consumption", dashboard.energy_consumption.get("target"))
            dashboard.water_usage["target"] = targets.get("water_usage", dashboard.water_usage.get("target"))
            dashboard.waste_generation["target"] = targets.get("waste_generation", dashboard.waste_generation.get("target"))
            dashboard.ghg_emissions["target"] = targets.get("ghg_emissions", dashboard.ghg_emissions.get("target"))
            dashboard.save()
            return dashboard
        except ObjectDoesNotExist:
            return {"error": "Dashboard not found"}

    def compare_with_benchmarks(self, dashboard_id, benchmarks):
        try:
            dashboard = SustainabilityDashboard.objects.get(id=dashboard_id)
            comparison = {
                "energy_consumption": {
                    "actual": dashboard.energy_consumption.get("actual", 0),
                    "benchmark": benchmarks.get("energy_consumption", 0)
                },
                "water_usage": {
                    "actual": dashboard.water_usage.get("actual", 0),
                    "benchmark": benchmarks.get("water_usage", 0)
                },
                "waste_generation": {
                    "actual": dashboard.waste_generation.get("actual", 0),
                    "benchmark": benchmarks.get("waste_generation", 0)
                },
                "ghg_emissions": {
                    "actual": dashboard.ghg_emissions.get("actual", 0),
                    "benchmark": benchmarks.get("ghg_emissions", 0)
                }
            }
            return comparison
        except ObjectDoesNotExist:
            return {"error": "Dashboard not found"}

    def generate_sustainability_report(self, dashboard_id):
        try:
            dashboard = SustainabilityDashboard.objects.get(id=dashboard_id)
            return {
                "user_id": dashboard.user.user_id,
                "energy_consumption": dashboard.energy_consumption,
                "water_usage": dashboard.water_usage,
                "waste_generation": dashboard.waste_generation,
                "ghg_emissions": dashboard.ghg_emissions
            }
        except ObjectDoesNotExist:
            return {"error": "Dashboard not found"}

class SustainabilityCertification(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    certification_type = models.CharField(max_length=255, choices=[('leed', 'Leed'), ('energy_star', 'Energy_start')], default='leed')
    status = models.CharField(max_length=255, choices=[('pending', 'Pending'), ('achieved', 'Achieved')], default='pending')
    submission_deadline = models.DateField()
    documentation = models.JSONField()

    def track_progress(self, certification_id):
        try:
            certification = SustainabilityCertification.objects.get(id=certification_id)
            return {
                "certification_type": certification.certification_type,
                "status": certification.status,
                "submission_deadline": certification.submission_deadline,
                "documentation": certification.documentation
            }
        except ObjectDoesNotExist:
            return {"error": "Certification not found"}

    def upload_documentation(self, certification_id, documentation):
        try:
            certification = SustainabilityCertification.objects.get(id=certification_id)
            certification.documentation.update(documentation)
            certification.save()
            return certification
        except ObjectDoesNotExist:
            return {"error": "Certification not found"}

    def update_status(self, certification_id, status):
        try:
            certification = SustainabilityCertification.objects.get(id=certification_id)
            certification.status = status
            certification.save()
            return certification
        except ObjectDoesNotExist:
            return {"error": "Certification not found"}

    def generate_certification_report(self, property_id):
        try:
            certifications = SustainabilityCertification.objects.filter(property=property_id)
            report = {
                "property_id": Property.property_id,
                "certifications": []
            }
            for cert in certifications:
                report["certifications"].append({
                    "certification_type": cert.certification_type,
                    "status": cert.status,
                    "submission_deadline": cert.submission_deadline,
                    "documentation": cert.documentation
                })
            return report
        except ObjectDoesNotExist:
            return {"error": "Certifications not found"}

class TenantSustainabilityResource(Resource):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, choices=[('energy_conservation', 'Energy Conservation'), ('waste_reduction', 'Waste Reduction')], default='energy_conservation')
    created_at = models.DateTimeField(auto_now_add=True)

    def add_resource(self, tenant_id, title, description, category):
        tenant_instance = Tenant.objects.get(id=tenant_id)
        resource = TenantSustainabilityResource(
            tenant=tenant_instance,
            title=title,
            description=description,
            category=category
        )
        resource.save()
        return resource

    def update_resource(self, resource_id, updates):
        try:
            resource = TenantSustainabilityResource.objects.get(id=resource_id)
            for attr, value in updates.items():
                setattr(resource, attr, value)
            resource.save()
            return resource
        except ObjectDoesNotExist:
            return {"error": "Resource not found"}

    def delete_resource(self, resource_id):
        try:
            resource = TenantSustainabilityResource.objects.get(id=resource_id)
            resource.delete()
            return {"success": True}
        except ObjectDoesNotExist:
            return {"success": False, "error": "Resource not found"}

    def generate_resource_report(self, tenant_id):
        resources = TenantSustainabilityResource.objects.filter(tenant_id=tenant_id)
        report = {
            "tenant_id": Tenant.user_id,
            "resources": []
        }
        for resource in resources:
            report["resources"].append({
                "title": resource.title,
                "description": resource.description,
                "category": resource.category,
                "created_at": resource.created_at
            })
        return report

class PropertySustainabilityRating(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rating_type = models.CharField(max_length=255)
    score = models.FloatField()
    issued_by = models.CharField(max_length=255)
    issued_date = models.DateField()

    def calculate_rating(self, property_id):
        property_instance = Property.objects.get(id=property_id)
        score = 85.0
        return score

    def update_rating(self, rating_id, score):
        try:
            rating = PropertySustainabilityRating.objects.get(id=rating_id)
            rating.score = score
            rating.save()
            return rating
        except ObjectDoesNotExist:
            return {"error": "Rating not found"}

    def delete_rating(self, rating_id):
        try:
            rating = PropertySustainabilityRating.objects.get(id=rating_id)
            rating.delete()
            return {"success": True}
        except ObjectDoesNotExist:
            return {"success": False, "error": "Rating not found"}

    def generate_rating_report(self, property_id):
        ratings = PropertySustainabilityRating.objects.filter(property_id=property_id)
        report = {
            "property_id": Property.property_id,
            "ratings": []
        }
        for rating in ratings:
            report["ratings"].append({
                "rating_type": rating.rating_type,
                "score": rating.score,
                "issued_by": rating.issued_by,
                "issued_date": rating.issued_date
            })
        return report

class SustainabilityForum(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=255)
    message = models.TextField()
    participants = models.ManyToManyField(Tenant, related_name='forums')
    timestamp = models.DateTimeField(auto_now_add=True)

    def create_forum(self, topic, message):
        forum = SustainabilityForum(
            topic=topic,
            message=message
        )
        forum.save()
        return forum

    def update_forum(self, forum_id, updates):
        try:
            forum = SustainabilityForum.objects.get(id=forum_id)
            for attr, value in updates.items():
                setattr(forum, attr, value)
            forum.save()
            return forum
        except ObjectDoesNotExist:
            return {"error": "Forum not found"}

    def delete_forum(self, forum_id):
        try:
            forum = SustainabilityForum.objects.get(id=forum_id)
            forum.delete()
            return {"success": True}
        except ObjectDoesNotExist:
            return {"success": False, "error": "Forum not found"}

    def get_forum_details(self, forum_id):
        try:
            forum = SustainabilityForum.objects.get(id=forum_id)
            return {
                "topic": forum.topic,
                "message": forum.message,
                "participants": [Tenant.user_id for Tenant.user_id in forum.participants.all()],
                "timestamp": forum.timestamp
            }
        except ObjectDoesNotExist:
            return {"error": "Forum not found"}

