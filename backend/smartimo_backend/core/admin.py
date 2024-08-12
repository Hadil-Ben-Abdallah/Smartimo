from django.contrib import admin
from core.models import Property, Notification, ClientInteraction, Communication, FinancialReport, SalesOpportunity, Resource, User, Document, Reminder, Portal

admin.site.register(Property)
admin.site.register(Notification)
admin.site.register(Reminder)
admin.site.register(ClientInteraction)
admin.site.register(Communication)
admin.site.register(FinancialReport)
admin.site.register(SalesOpportunity)
admin.site.register(Resource)
admin.site.register(User)
admin.site.register(Document)
admin.site.register(Portal)
