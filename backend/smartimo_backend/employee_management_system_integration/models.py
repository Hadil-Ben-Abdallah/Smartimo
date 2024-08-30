from django.db import models
from lease_rental_management.models import PropertyManager

class Permission(models.Model):
    id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def create_permission(self, name, description):
        self.permission_name = name
        self.description = description
        self.save()
        return self

    def modify_permission(self, permission_id, new_description):
        permission = Permission.objects.get(id=permission_id)
        permission.description = new_description
        permission.save()

    def delete_permission(self, permission_id):
        permission = Permission.objects.get(id=permission_id)
        permission.delete()


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255, blank=True, null=True)
    permissions = models.ManyToManyField(Permission, blank=True, null=True)

    def define_role(self, name, permissions):
        self.role_name = name
        self.permissions.set(permissions)
        self.save()
        return self

    def modify_role_permissions(self, role_id, new_permissions):
        role = Role.objects.get(id=role_id)
        role.permissions.set(new_permissions)
        role.save()

    def assign_role(self, employee_id, role_id):
        employee = EmployeeProfile.objects.get(id=employee_id)
        role = Role.objects.get(id=role_id)
        employee.role_id = role
        employee.save()


class EmployeeProfile(models.Model):
    employment_history = models.TextField(blank=True, null=True)
    performance_records = models.TextField(blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def view_profile(self):
        return {
            'employment_history': self.employment_history,
            'performance_records': self.performance_records,
            'role_id': self.role.role_name,
        }

    def update_contact_information(self, new_contact_info):
        for key, value in new_contact_info.items():
            setattr(self, key, value)
        self.save()

    def get_employment_history(self):
        return self.employment_history

    def get_performance_records(self):
        return self.performance_records


class HRISIntegration(models.Model):
    employee_records = models.TextField(blank=True, null=True)
    hris_system = models.CharField(max_length=255, blank=True, null=True)

    def sync_employee_data(self):
        self.employee_records = "Synced data from HRIS"
        self.save()

    def trigger_onboarding_workflow(self, employee_id):
        onboarding_steps = f"Onboarding process started for employee {employee_id}"
        return onboarding_steps

    def trigger_offboarding_workflow(self, employee_id):
        offboarding_steps = f"Offboarding process started for employee {employee_id}"
        return offboarding_steps

# EmployeeSelfService model
class EmployeeSelfService(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    personal_information = models.TextField(blank=True, null=True)
    work_schedule = models.TextField(blank=True, null=True)
    performance_goals = models.TextField(blank=True, null=True)

    def view_personal_information(self):
        return self.personal_information

    def update_personal_information(self, new_info):
        self.personal_information = new_info
        self.save()

    def view_work_schedule(self):
        return self.work_schedule

    def submit_time_off_request(self, dates):
        request = f"Time-off request for dates {dates} submitted."
        return request

    def set_performance_goals(self, goals):
        self.performance_goals = goals
        self.save()

    def track_performance_progress(self):
        progress = f"Tracking progress on goals: {self.performance_goals}"
        return progress

# AttendanceTracking model
class AttendanceTracking(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    clock_in_out_data = models.TextField(blank=True, null=True)
    work_hours = models.FloatField(blank=True, null=True)
    attendance_records = models.TextField(blank=True, null=True)

    def import_attendance_data(self):
        self.attendance_records = "Imported attendance data"
        self.save()

    def generate_timesheets(self):
        timesheets = f"Timesheets for {self.employee} generated"
        return timesheets

    def analyze_attendance_patterns(self):
        patterns = f"Attendance patterns for {self.employee} analyzed"
        return patterns

    def send_attendance_alerts(self):
        alerts = f"Attendance alerts sent for {self.employee}"
        return alerts


class PerformanceManagement(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    performance_goals = models.TextField(blank=True, null=True)
    performance_reviews = models.TextField(blank=True, null=True)
    development_plans = models.TextField(blank=True, null=True)

    def conduct_performance_review(self, employee_id):
        review = f"Performance review conducted for employee {employee_id}"
        return review

    def set_development_plan(self, employee_id, plan):
        self.development_plans = plan
        self.save()

    def track_review_cycles(self):
        cycles = f"Tracking review cycles for {self.employee}"
        return cycles

    def capture_feedback(self, employee_id, feedback):
        feedback_entry = f"Feedback for {employee_id}: {feedback}"
        return feedback_entry

    def identify_high_potential_employees(self):
        potential_employees = "High-potential employees identified"
        return potential_employees


class RoleBasedAccessControl(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    access_levels = models.TextField(blank=True, null=True)

    def define_access_levels(self, role_id, access_levels):
        self.role = Role.objects.get(role=role_id)
        self.access_levels = access_levels
        self.save()

    def assign_access_levels(self, employee_id, access_levels):
        rbac = RoleBasedAccessControl.objects.get(employee=employee_id)
        rbac.access_levels = access_levels
        rbac.save()

    def modify_access_levels(self, role_id, new_access_levels):
        rbac = RoleBasedAccessControl.objects.get(role=role_id)
        rbac.access_levels = new_access_levels
        rbac.save()

    def revoke_access(self, employee_id):
        rbac = RoleBasedAccessControl.objects.get(employee=employee_id)
        rbac.delete()


class TalentManagement(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    career_path = models.TextField(blank=True, null=True)
    succession_plan = models.TextField(blank=True, null=True)
    skills_development = models.TextField(blank=True, null=True)

    def plan_career_path(self, employee_id, career_path):
        self.career_path = career_path
        self.save()

    def create_succession_plan(self, employee_id, plan):
        self.succession_plan = plan
        self.save()

    def track_skills_development(self, employee_id, skills):
        self.skills_development = skills
        self.save()

    def identify_leadership_candidates(self):
        candidates = "Leadership candidates identified"
        return candidates


class DepartmentManager(models.Model):
    manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    department = models.CharField(max_length=255, blank=True, null=True)
    employees = models.ManyToManyField(EmployeeProfile, blank=True, null=True)
    roles = models.ManyToManyField(Role, blank=True, null=True)

    def assign_roles(self, employee_id, role_id):
        role = Role.objects.get(role_id=role_id)
        employee = EmployeeProfile.objects.get(id=employee_id)
        employee.role = role
        employee.save()

    def modify_permissions(self, role_id, new_permissions):
        role = Role.objects.get(role_id=role_id)
        role.modify_role_permissions(role_id, new_permissions)

    def track_employee_performance(self, employee_id):
        employee = EmployeeProfile.objects.get(id=employee_id)
        performance = employee.get_performance_records()
        return performance

    def generate_reports(self):
        report = "Department performance and employee metrics report generated"
        return report

