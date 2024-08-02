# from django.contrib import admin
# from django_tenants.admin import TenantAdminMixin
# from .models import Client, Interaction, Reminder, ClientAnalytics, ClientRealEstateAgent

# class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', 'phone', 'address', 'created_at', 'updated_at')
#     search_fields = ('name', 'email', 'phone')
#     list_filter = ('created_at', 'updated_at')

# class InteractionAdmin(TenantAdminMixin, admin.ModelAdmin):
#     list_display = ('id', 'client_id', 'agent_id', 'type', 'timestamp')
#     search_fields = ('type', 'details')
#     list_filter = ('timestamp',)

# class ReminderAdmin(TenantAdminMixin, admin.ModelAdmin):
#     list_display = ('id', 'client_id', 'agent_id', 'task', 'due_date', 'status', 'created_at', 'updated_at')
#     search_fields = ('task', 'status')
#     list_filter = ('status', 'due_date', 'created_at', 'updated_at')

# class ClientAnalyticsAdmin(TenantAdminMixin, admin.ModelAdmin):
#     list_display = ('client_id', 'engagement_metrics')

# class ClientRealEstateAgentAdmin(TenantAdminMixin, admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', 'phone')
#     search_fields = ('name', 'email', 'phone')
#     list_filter = ('name',)
#     filter_horizontal = ('clients',)

# admin.site.register(Client, ClientAdmin)
# admin.site.register(Interaction, InteractionAdmin)
# admin.site.register(Reminder, ReminderAdmin)
# admin.site.register(ClientAnalytics, ClientAnalyticsAdmin)
# admin.site.register(ClientRealEstateAgent, ClientRealEstateAgentAdmin)
