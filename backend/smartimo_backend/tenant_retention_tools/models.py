from django.db import models
from lease_rental_management.models import Tenant
from core.models import Feedback, TimeStampedModel
from complaints_and_resolution_system.models import Complaint

class LoyaltyTier(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    min_points = models.IntegerField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)

    def update_tier(self, name: str, min_points: int, benefits: list):
        self.name = name
        self.min_points = min_points
        self.benefits = ', '.join(benefits)
        self.save()

    def get_tier_details(self):
        return {
            "tier_id": self.id,
            "name": self.name,
            "min_points": self.min_points,
            "benefits": self.benefits.split(', ')
        }

class LoyaltyProgram(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    tiers = models.ManyToManyField(LoyaltyTier, related_name="programs")
    point_system = models.TextField(blank=True, null=True)
    reward_criteria = models.TextField(blank=True, null=True)

    def create_tier(self, tier: LoyaltyTier):
        self.tiers.add(tier)
        self.save()

    def define_point_system(self, description: str):
        self.point_system = description
        self.save()

    def set_reward_criteria(self, criteria: str):
        self.reward_criteria = criteria
        self.save()

    def get_program_details(self):
        return {
            "program_id": self.id,
            "name": self.name,
            "tiers": [tier.get_tier_details() for tier in self.tiers.all()],
            "point_system": self.point_system,
            "reward_criteria": self.reward_criteria
        }

class TenantLoyalty(Tenant):
    loyalty_program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE)
    points = models.IntegerField(default=0, blank=True, null=True)
    enrolled_tiers = models.ManyToManyField(LoyaltyTier, related_name="enrolled_tenants")
    maintenance_requests = models.ManyToManyField(LoyaltyTier, related_name="maintenance_requests")

    def submit_complaint(self, complaint: str):
        Complaint.objects.create(tenant=self.user_id, description=complaint)

    def enroll_in_program(self, program: LoyaltyProgram):
        self.loyalty_program = program
        self.save()

    def view_loyalty_status(self):
        return {
            "tenant": self.username,
            "program": self.loyalty_program.get_program_details(),
            "points": self.points,
            "enrolled_tiers": [tier.get_tier_details() for tier in self.enrolled_tiers.all()],
        }

class Incentive(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    eligibility_criteria = models.TextField(blank=True, null=True)
    promotion_period = models.CharField(max_length=100, blank=True, null=True)

    def create_incentive(self, type: str, amount: float, criteria: str, period: str):
        self.type = type
        self.amount = amount
        self.eligibility_criteria = criteria
        self.promotion_period = period
        self.save()

    def get_incentive_details(self):
        return {
            "incentive_id": self.id,
            "type": self.type,
            "amount": self.amount,
            "eligibility_criteria": self.eligibility_criteria,
            "promotion_period": self.promotion_period,
        }

class LoyaltyFeedback(Feedback):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

    def submit_feedback(self, feedback_text: str, rating: int):
        self.comments = feedback_text
        self.rating = rating
        self.save()

    def get_feedback_details(self):
        return {
            "tenant": self.tenant.username,
            "event_id": self.event,
            "feedback_text": self.comments,
            "rating": self.rating
        }

