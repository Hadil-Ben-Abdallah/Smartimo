from django.db import models
from core.models import Property, TimeStampedModel
from lease_rental_management.models import Tenant

class Vacancy(Property):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10, choices=[('vacant', 'Vacant'), ('occupied', 'Occupied')], default='vacant')

    def update_status(self, status):
        if status in dict(self.status).keys():
            self.status = status
            self.save()
        else:
            raise ValueError("Invalid status")

    def get_vacancy_details(self):
        return {
            "id": self.id,
            "property": self.property_id,
            "status": self.status,
        }

    @classmethod
    def list_vacancies(cls):
        return cls.objects.all()


class VacancyMarketingCampaign(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    platforms = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    photos = models.JSONField(blank=True, null=True)
    virtual_tours = models.JSONField(blank=True, null=True)
    rental_terms = models.TextField(blank=True, null=True)

    def create_campaign(self, vacancy, platforms, description, photos, virtual_tours, rental_terms):
        return VacancyMarketingCampaign.objects.create(
            vacancy=vacancy,
            platforms=platforms,
            description=description,
            photos=photos,
            virtual_tours=virtual_tours,
            rental_terms=rental_terms
        )

    def edit_campaign(self, platforms=None, description=None, photos=None, virtual_tours=None, rental_terms=None):
        if platforms:
            self.platforms = platforms
        if description:
            self.description = description
        if photos:
            self.photos = photos
        if virtual_tours:
            self.virtual_tours = virtual_tours
        if rental_terms:
            self.rental_terms = rental_terms
        self.save()
        return self

    def delete_campaign(self):
        self.delete()

    def get_campaign_details(self):
        return {
            "id": self.id,
            "vacancy": self.vacancy.id,
            "platforms": self.platforms,
            "description": self.description,
            "photos": self.photos,
            "virtual_tours": self.virtual_tours,
            "rental_terms": self.rental_terms
        }

    @classmethod
    def list_campaigns(cls):
        return cls.objects.all()

    def track_performance(self):
        return {"status": "Performance tracking is not yet implemented"}


class ProspectiveTenant(Tenant):
    preferences = models.JSONField(blank=True, null=True)
    saved_listings = models.ManyToManyField(Vacancy, through='SavedListing')

    def search_properties(self, search_criteria):
        return Vacancy.objects.filter(**search_criteria)

    def save_listing(self, vacancy):
        if not self.saved_listings.filter(id=vacancy.id).exists():
            self.saved_listings.add(vacancy)

    def subscribe_notifications(self):
        return {"status": "Notification subscription not yet implemented"}

    @classmethod
    def list_saved_listings(cls):
        return cls.saved_listings.all()


class ViewingAppointment(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    date_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    prospective_tenant = models.ForeignKey(ProspectiveTenant, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='scheduled')

    def schedule_appointment(self, vacancy, date_time, duration, prospective_tenant):
        return ViewingAppointment.objects.create(
            vacancy=vacancy,
            date_time=date_time,
            duration=duration,
            prospective_tenant=prospective_tenant,
            status='scheduled'
        )

    def reschedule_appointment(self, new_date_time):
        self.date_time = new_date_time
        self.save()

    def cancel_appointment(self):
        self.status = 'canceled'
        self.save()

    def send_invitation(self):
        return {"status": "Invitation sending not yet implemented"}

    @classmethod
    def list_appointments(cls):
        return cls.objects.all()


class LeaseNegotiation(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    prospective_tenant = models.ForeignKey(ProspectiveTenant, on_delete=models.CASCADE)
    terms = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('ongoing', 'Ongoing'), ('finalized', 'Finalized')], default='ongoing')

    def initiate_negotiation(self, vacancy, prospective_tenant, terms):
        return LeaseNegotiation.objects.create(
            vacancy=vacancy,
            prospective_tenant=prospective_tenant,
            terms=terms,
            status='ongoing'
        )

    def update_negotiation(self, terms):
        self.terms = terms
        self.save()

    def finalize_negotiation(self):
        self.status = 'finalized'
        self.save()

    def send_message(self, message):
        return {"status": "Message sending not yet implemented"}

    @classmethod
    def list_negotiations(cls):
        return cls.objects.filter(status='ongoing')


class TenantScreening(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    prospective_tenant = models.ForeignKey(ProspectiveTenant, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    report = models.TextField(blank=True, null=True)

    def initiate_screening(self, prospective_tenant):
        return TenantScreening.objects.create(
            prospective_tenant=prospective_tenant,
            status='pending'
        )

    def get_screening_report(self):
        return self.report

    def update_screening_status(self, status):
        if status in dict(self.status).keys():
            self.status = status
            self.save()
        else:
            raise ValueError("Invalid status")

    @classmethod
    def list_screenings(cls):
        return cls.objects.all()


class VacancyAnalytics(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    vacancy_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    time_to_fill = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def generate_report(self):
        return {
            "analytics_id": self.id,
            "vacancy": self.vacancy.id,
            "vacancy_rate": self.vacancy_rate,
            "time_to_fill": self.time_to_fill,
            "conversion_rate": self.conversion_rate
        }

    def get_analytics_details(self):
        return self.generate_report()

    @classmethod
    def list_analytics(cls):
        return cls.objects.all()

    def benchmark_performance(self):
        return {"status": "Performance benchmarking not yet implemented"}

    def identify_trends(self):
        return {"status": "Trend identification not yet implemented"}

