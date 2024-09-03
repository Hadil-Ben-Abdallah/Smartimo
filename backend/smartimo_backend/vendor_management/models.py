from django.db import models
from core.models import Communication, TimeStampedModel
from lease_rental_management.models import PropertyManager
from django.utils import timezone


class Vendor(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null= True)
    email = models.EmailField(blank=True, null= True)
    phone = models.CharField(max_length=20, blank=True, null= True)
    certifications = models.JSONField(default=list, blank=True, null= True)
    service_specialties = models.JSONField(default=list, blank=True, null= True)
    insurance_details = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, blank=True, null= True)
    reviews = models.JSONField(default=list, blank=True, null= True)
    documents = models.JSONField(default=list, blank=True, null= True)
    pricing_model = models.CharField(max_length=50, blank=True, null= True)
    service_areas = models.JSONField(default=list, blank=True, null= True)
    availability = models.JSONField(default=dict, blank=True, null= True)
    profile_content = models.JSONField(default=dict, blank=True, null= True)

    def create_profile(self):
        self.profile_content = {
            "certifications": self.certifications,
            "service_specialties": self.service_specialties,
            "insurance_details": self.insurance_details,
            "pricing_model": self.pricing_model,
            "service_areas": self.service_areas,
            "availability": self.availability
        }
        self.save()

    def upload_documents(self, document_files):
        self.documents.extend(document_files)
        self.save()

    def update_profile(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        self.create_profile()

    def get_profile_details(self):
        return self.profile_content

    def calculate_rating(self):
        if not self.reviews:
            return 0.00
        total_rating = sum(review['rating'] for review in self.reviews)
        return round(total_rating / len(self.reviews), 2)

    def upload_media(self, media_files):
        media_content = self.profile_content.get("media", [])
        media_content.extend(media_files)
        self.profile_content["media"] = media_content
        self.save()

    def update_availability(self, new_availability):
        self.availability = new_availability
        self.save()


class VendorsPropertyManager(PropertyManager):
    managed_vendors = models.ManyToManyField(Vendor, related_name='managed_by')

    def onboard_vendor(self, vendor):
        if not self.managed_vendors.filter(id=Vendor.id).exists():
            self.managed_vendors.add(vendor)
            self.save()

    def search_vendors(self, **criteria):
        vendors = Vendor.objects.all()
        for key, value in criteria.items():
            if hasattr(Vendor, key):
                vendors = vendors.filter(**{key: value})
        return vendors

    def manage_contracts(self, contract_details):
        contract = Contract.objects.create(**contract_details, property_manager=self)
        return contract

    def track_performance(self):
        performance_data = {}
        for vendor in self.managed_vendors.all():
            performance_data[Vendor.id] = vendor.performancemetrics_set.all()
        return performance_data

    def communicate_with_vendors(self, vendor, message):
        VendorsCommunication.objects.create(
            sender=self,
            receiver=vendor,
            message=message,
            status="Sent"
        )


class Contract(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(VendorsPropertyManager, on_delete=models.CASCADE)
    scope_of_work = models.TextField(blank=True, null= True)
    pricing = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null= True)
    payment_terms = models.TextField(blank=True, null= True)
    sla = models.TextField(blank=True, null= True)
    document_version = models.IntegerField(default=1, blank=True, null= True)
    expiry_date = models.DateField(blank=True, null= True)
    status = models.CharField(max_length=20, blank=True, null= True)

    def create_contract(self):
        self.save()

    def update_contract(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        self.save()

    def renew_contract(self):
        self.expiry_date = timezone.now().date() + timezone.timedelta(days=365)

    def track_contract_status(self):
        return {
            "status": self.status,
            "expiry_date": self.expiry_date
        }

    def get_contract_details(self):
        return {
            "vendor": self.vendor.id,
            "property_manager": self.property_manager.user_id,
            "scope_of_work": self.scope_of_work,
            "pricing": self.pricing,
            "payment_terms": self.payment_terms,
            "sla": self.sla,
            "document_version": self.document_version,
            "expiry_date": self.expiry_date,
            "status": self.status
        }


class PerformanceMetrics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    response_time = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null= True)
    resolution_time = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null= True)
    customer_satisfaction_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null= True)
    compliance_sla = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null= True)
    feedback = models.JSONField(default=list, blank=True, null= True)

    def track_metrics(self):
        self.save()

    def generate_report(self):
        report = {
            "response_time": self.response_time,
            "resolution_time": self.resolution_time,
            "customer_satisfaction_score": self.customer_satisfaction_score,
            "compliance_sla": self.compliance_sla,
            "feedback": self.feedback
        }
        return report

    def calculate_kpi(self):
        kpi = {
            "average_response_time": self.response_time,
            "average_resolution_time": self.resolution_time,
            "average_customer_satisfaction": self.customer_satisfaction_score,
            "sla_compliance_rate": self.compliance_sla
        }
        return kpi

    def get_performance_details(self):
        return {
            "response_time": self.response_time,
            "resolution_time": self.resolution_time,
            "customer_satisfaction_score": self.customer_satisfaction_score,
            "compliance_sla": self.compliance_sla,
            "feedback": self.feedback
        }

    def compare_vendors(self, other_vendor_performance):
        pass


class VendorsCommunication(Communication):
    sender = models.ForeignKey(VendorsPropertyManager, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='received_messages')
    status = models.CharField(max_length=20, choices=[('sent', 'Sent'), ('received', 'Received'), ('read', 'Read'), ('resolved', 'Resolved')], default='sent')

    def get_message_history(self):
        return VendorsCommunication.objects.filter(sender=self.sender, receiver=self.receiver).order_by('-id')

    def track_communication_status(self):
        return self.status

    def resolve_dispute(self):
        self.status = "Resolved"
        self.save()

