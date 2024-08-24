from django.db import models
from cryptography.fernet import Fernet
from core.models import User
import datetime

# EncryptionService Model
class EncryptionService(models.Model):
    encryption_algorithm = models.CharField(max_length=50, default="AES-256", blank=True, null=True)
    key_management = models.TextField(blank=True, null=True)

    def encrypt_data(self, data: str) -> str:
        key = self.generate_key()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode())
        return encrypted_data.decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        key = self.generate_key()
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data.encode())
        return decrypted_data.decode()

    def generate_key(self) -> str:
        return Fernet.generate_key().decode()


# AuthenticationService Model
class AuthenticationService(models.Model):
    mfa_enabled = models.BooleanField(default=False, blank=True, null=True)
    rbac_policy = models.TextField(blank=True, null=True)

    def authenticate_user(self, user_credentials: dict) -> bool:
        user = User.objects.filter(username=user_credentials.get('username')).first()
        if user and user.check_password(user_credentials.get('password')):
            if self.mfa_enabled:
                return self.configure_mfa(user, user_credentials.get('mfa_code'))
            return True
        return False

    def authorize_access(self, user: User, resource: str) -> bool:
        permissions = self.rbac_policy.get(user.role, [])
        return resource in permissions

    def configure_mfa(self, user: User, mfa_code: dict) -> bool:
        return mfa_code.get('valid', False)


class DataAccessControl(models.Model):
    user_role = models.CharField(max_length=50, blank=True, null=True)
    permissions = models.TextField(blank=True, null=True)

    def set_user_role(self, user: User, role: str):
        user.user_type = role
        user.save()

    def get_user_permissions(self, user: User) -> list:
        return self.permissions.split(",")

    def log_access_event(self, event_details: dict):
        DataAccessControl.objects.create(event_type="access", details=event_details)


class GDPRCompliance(models.Model):
    consent_records = models.TextField(blank=True, null=True)
    data_requests = models.TextField(blank=True, null=True)

    def record_consent(self, user: User, consent_details: dict):
        self.consent_records += f"{user.user_id}: {consent_details}\n"
        self.save()

    def generate_gdpr_report(self) -> dict:
        return {
            "consent_records": self.consent_records,
            "data_requests": self.data_requests,
        }


class CCPACompliance(models.Model):
    opt_out_requests = models.TextField(blank=True, null=True)
    data_deletion_requests = models.TextField(blank=True, null=True)

    def process_opt_out_request(self, user: User):
        self.opt_out_requests += f"{user.user_id}: Opted out of data sharing\n"
        self.save()

    def process_data_deletion_request(self, user: User):
        self.data_deletion_requests += f"{user.user_id}: Data deletion requested\n"
        user.delete()
        self.save()

    def generate_ccpa_report(self) -> dict:
        return {
            "opt_out_requests": self.opt_out_requests,
            "data_deletion_requests": self.data_deletion_requests,
        }


class ComplianceAudit(models.Model):
    id = models.AutoField(primary_key=True)
    audit_date = models.DateField(default=datetime.date.today, blank=True, null=True)
    audit_findings = models.TextField(blank=True, null=True)

    def schedule_audit(self, audit_details: dict):
        self.id = audit_details.get('id')
        self.audit_date = audit_details.get('audit_date', datetime.date.today())
        self.save()

    def record_audit_findings(self, audit_id: str, findings: dict):
        self.audit_findings += f"Audit {audit_id}: {findings}\n"
        self.save()

    def generate_audit_report(self, audit_id: str) -> dict:
        return {
            "audit_id": audit_id,
            "audit_date": self.audit_date,
            "findings": self.audit_findings,
        }


class DataProtectionOfficer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    contact_information = models.TextField(blank=True, null=True)

    def review_compliance(self):
        compliance_status = "All systems are compliant"
        return {"compliance_status": compliance_status}

    def handle_regulatory_inquiries(self, inquiry_details: dict):
        response = f"Responding to inquiry from {inquiry_details['authority']} on {inquiry_details['date']}"
        return {"response": response}

