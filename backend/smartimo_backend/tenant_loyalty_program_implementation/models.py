from django.db import models
from django.utils import timezone
from lease_rental_management.models import Tenant

class TenantLoyaltyProgram(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    eligibility_criteria = models.JSONField(blank=True, null=True)
    reward_tiers = models.JSONField(blank=True, null=True)
    earning_mechanisms = models.JSONField(blank=True, null=True)
    point_accrual_rates = models.JSONField(blank=True, null=True)
    redemption_thresholds = models.JSONField(blank=True, null=True)
    expiration_policies = models.JSONField(blank=True, null=True)

    def define_rules(self, name, eligibility_criteria, reward_tiers, earning_mechanisms, point_accrual_rates, redemption_thresholds, expiration_policies):
        self.name = name
        self.eligibility_criteria = eligibility_criteria
        self.reward_tiers = reward_tiers
        self.earning_mechanisms = earning_mechanisms
        self.point_accrual_rates = point_accrual_rates
        self.redemption_thresholds = redemption_thresholds
        self.expiration_policies = expiration_policies
        self.save()

    def customize_settings(self, point_accrual_rates, redemption_thresholds, expiration_policies):
        self.point_accrual_rates = point_accrual_rates
        self.redemption_thresholds = redemption_thresholds
        self.expiration_policies = expiration_policies
        self.save()

    def adjust_program(self, eligibility_criteria=None, reward_tiers=None, earning_mechanisms=None):
        if eligibility_criteria is not None:
            self.eligibility_criteria = eligibility_criteria
        if reward_tiers is not None:
            self.reward_tiers = reward_tiers
        if earning_mechanisms is not None:
            self.earning_mechanisms = earning_mechanisms
        self.save()

    def get_program_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "eligibility_criteria": self.eligibility_criteria,
            "reward_tiers": self.reward_tiers,
            "earning_mechanisms": self.earning_mechanisms,
            "point_accrual_rates": self.point_accrual_rates,
            "redemption_thresholds": self.redemption_thresholds,
            "expiration_policies": self.expiration_policies,
        }

class TenantLoyaltyStatus(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    program = models.ForeignKey(TenantLoyaltyProgram, on_delete=models.CASCADE)
    points_balance = models.IntegerField(default=0, blank=True, null=True)
    reward_eligibility = models.JSONField(blank=True, null=True)
    enrollment_date = models.DateField(default=timezone.now)

    def enroll_tenant(self, tenant, program):
        self.tenant = tenant
        self.program = program
        self.points_balance = 0
        self.reward_eligibility = {"eligibility_status": "eligible"}
        self.save()

    def track_progress(self):
        return {
            "points_balance": self.points_balance,
            "reward_eligibility": self.reward_eligibility,
            "enrollment_date": self.enrollment_date,
        }

    def get_status_details(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant.user_id,
            "program_id": self.program.id,
            "points_balance": self.points_balance,
            "reward_eligibility": self.reward_eligibility,
            "enrollment_date": self.enrollment_date,
        }

class LoyaltyReward(models.Model):
    id = models.AutoField(primary_key=True)
    program = models.ForeignKey(TenantLoyaltyProgram, on_delete=models.CASCADE)
    reward_name = models.CharField(max_length=255, blank=True, null=True)
    reward_description = models.TextField(blank=True, null=True)
    points_required = models.IntegerField(blank=True, null=True)
    availability_status = models.CharField(max_length=50, blank=True, null=True)

    def define_reward(self, reward_name, reward_description, points_required, availability_status):
        self.reward_name = reward_name
        self.reward_description = reward_description
        self.points_required = points_required
        self.availability_status = availability_status
        self.save()

    def update_reward(self, reward_name=None, reward_description=None, points_required=None, availability_status=None):
        if reward_name is not None:
            self.reward_name = reward_name
        if reward_description is not None:
            self.reward_description = reward_description
        if points_required is not None:
            self.points_required = points_required
        if availability_status is not None:
            self.availability_status = availability_status
        self.save()

    def distribute_reward(self):
        if TenantLoyaltyStatus.points_balance >= self.points_required and self.availability_status == 'available':
            TenantLoyaltyStatus.points_balance -= self.points_required
            TenantLoyaltyStatus.save()
            self.availability_status = 'distributed'
            self.save()
            return True
        return False

    def track_redemption(self):
        return {
            "reward_name": self.reward_name,
            "points_required": self.points_required,
            "availability_status": self.availability_status,
            "tenant_points_balance": TenantLoyaltyStatus.points_balance,
        }

    def get_reward_details(self):
        return {
            "id": self.id,
            "program_id": self.program.id,
            "reward_name": self.reward_name,
            "reward_description": self.reward_description,
            "points_required": self.points_required,
            "availability_status": self.availability_status,
        }

class RewardRedemption(models.Model):
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    reward = models.ForeignKey(LoyaltyReward, on_delete=models.CASCADE)
    redemption_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def redeem_reward(self, tenant, reward):
        self.tenant = tenant
        self.reward = reward
        self.redemption_date = timezone.now()
        self.status = 'pending'
        self.save()

    def confirm_redemption(self):
        self.status = 'completed'
        self.save()

    def get_redemption_details(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant.user_id,
            "reward_id": self.reward.id,
            "redemption_date": self.redemption_date,
            "status": self.status,
        }

class LoyaltyProgramAnalytics(models.Model):
    id = models.AutoField(primary_key=True)
    program = models.ForeignKey(TenantLoyaltyProgram, on_delete=models.CASCADE)
    tenant_participation_rate = models.FloatField(blank=True, null=True)
    lease_renewal_rate = models.FloatField(blank=True, null=True)
    tenant_satisfaction_score = models.FloatField(blank=True, null=True)
    reward_utilization = models.FloatField(blank=True, null=True)
    roi_metrics = models.FloatField(blank=True, null=True)

    def generate_report(self):
        return {
            "tenant_participation_rate": self.tenant_participation_rate,
            "lease_renewal_rate": self.lease_renewal_rate,
            "tenant_satisfaction_score": self.tenant_satisfaction_score,
            "reward_utilization": self.reward_utilization,
            "roi_metrics": self.roi_metrics,
        }

    def track_kpis(self):
        return {
            "tenant_participation_rate": self.tenant_participation_rate,
            "lease_renewal_rate": self.lease_renewal_rate,
            "tenant_satisfaction_score": self.tenant_satisfaction_score,
            "reward_utilization": self.reward_utilization,
            "roi_metrics": self.roi_metrics,
        }

    def perform_cohort_analysis(self):
        return {
            "cohort_analysis": "Not yet implemented"
        }

    def get_analytics_details(self):
        return {
            "id": self.id,
            "program_id": self.program.id,
            "tenant_participation_rate": self.tenant_participation_rate,
            "lease_renewal_rate": self.lease_renewal_rate,
            "tenant_satisfaction_score": self.tenant_satisfaction_score,
            "reward_utilization": self.reward_utilization,
            "roi_metrics": self.roi_metrics,
        }

