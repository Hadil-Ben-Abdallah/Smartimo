from django.contrib import admin
from django.urls import path, include
from schema_graph.views import Schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("schema/", Schema.as_view()),
    path('api/core/', include('core.urls')),
    path('api/property-listing/', include('property_listing.urls')),
    path('api/client-management/', include('client_management.urls')),
    path('api/lease-rental-management/', include('lease_rental_management.urls')),
    path('api/sales-management/', include('sales_management.urls')),
    path('api/document-management/', include('document_management.urls')),
    path('api/financial-management/', include('financial_management.urls')),
    path('api/task-calendar-management/', include('task_calendar_management.urls')),
    path('api/communication-tools/', include('communication_tools.urls')),
    path('api/reporting-and-analytics/', include('reporting_and_analytics.urls')),
    path('api/maintenance-and-service-requests/', include('maintenance_and_service_requests.urls')),
    path('api/vendor-management/', include('vendor_management.urls')),
    path('api/marketplace-integration/', include('marketplace_integration.urls')),
    path('api/CRM-integration/', include('CRM_integration.urls')),
    path('api/marketing-tools-integration/', include('marketing_tools_integration.urls')),
    path('api/compliance-and-legal-management/', include('compliance_and_legal_management.urls')),
    path('api/mobile-app-development/', include('mobile_app_development.urls')),
    path('api/tenant-portal-development/', include('tenant_portal_development.urls')),
    path('api/owner-portal-development/', include('owner_portal_development.urls')),
    path('api/lead-management/', include('lead_management.urls')),
    path('api/visitor-management-for-property-access/', include('visitor_management_for_property_access.urls')),
    path('api/community-management-features/', include('community_management_features.urls')),
    path('api/feedback-and-review-system/', include('feedback_and_review_system.urls')),
    path('api/integration-with-accounting-software/', include('integration_with_accounting_software.urls')),
    path('api/predictive-analytics-for-market-insights/', include('predictive_analytics_for_market_insights.urls')),
    path('api/energy-management/', include('energy_management.urls')),
    path('api/sustainability-tracking/', include('sustainability_tracking.urls')),
    path('api/remote-property-monitoring/', include('remote_property_monitoring.urls')),
    path('api/customizable-reporting-for-tailored-insights/', include('customizable_reporting_for_tailored_insights.urls')),
    path('api/forecasting-and-demand-planning/', include('forecasting_and_demand_planning.urls')),
]






