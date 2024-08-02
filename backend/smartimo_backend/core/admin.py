from django.contrib import admin
from core.models import Property, Notification, ClientInteraction, Communication, PropertyListing, FinancialReport, SalesOpportunity, Resource, User, Vendor

admin.site.register(Property)
admin.site.register(Notification)
admin.site.register(ClientInteraction)
admin.site.register(Communication)
# admin.site.register(LeaseAgreement)
admin.site.register(PropertyListing)
admin.site.register(FinancialReport)
admin.site.register(SalesOpportunity)
admin.site.register(Resource)
admin.site.register(User)
admin.site.register(Vendor)
