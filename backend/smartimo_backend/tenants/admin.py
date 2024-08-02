from django.contrib import admin
from tenants.models import Tenant, Domain

admin.site.register(Tenant)
admin.site.register(Domain)
