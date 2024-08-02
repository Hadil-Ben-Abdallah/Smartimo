from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    auto_create_schema = True

class Domain(DomainMixin):
    pass

