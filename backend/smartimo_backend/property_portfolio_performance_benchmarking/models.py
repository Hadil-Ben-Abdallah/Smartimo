from django.db import models
from django.utils import timezone
import numpy as np
from property_performance_benchmarking_integration.models import PropertyPerformance
from property_listing.models import PropertyOwner
from core.models import Property

class PerformanceBenchmark(models.Model):
    id = models.AutoField(primary_key=True)
    benchmark_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    date_collected = models.DateTimeField(default=timezone.now, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)

    def update_value(self, new_value):
        self.value = new_value
        self.date_collected = timezone.now()
        self.save()

    def get_benchmark_info(self):
        return {
            'benchmark_name': self.benchmark_name,
            'description': self.description,
            'value': self.value,
            'date_collected': self.date_collected,
            'source': self.source
        }

class PropertyPortfolioPerformance(PropertyPerformance):
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE)
    rental_income = models.FloatField(blank=True, null=True)
    net_operating_income = models.FloatField(blank=True, null=True)
    cap_rate = models.FloatField(blank=True, null=True)
    irr = models.FloatField(blank=True, null=True)
    valuation = models.FloatField(blank=True, null=True)
    price_per_sqft = models.FloatField(blank=True, null=True)
    date_collected = models.DateTimeField(default=timezone.now, blank=True, null=True)
        
    def calculate_roi(self):
        if self.valuation == 0:
            return 0
        roi = (self.rental_income / self.valuation) * 100
        return round(roi, 2)

    def calculate_cap_rate(self):
        if self.valuation == 0:
            return 0
        cap_rate = (self.net_operating_income / self.valuation) * 100
        return round(cap_rate, 2)
    
    def calculate_irr(self, initial_investment, cash_flows):
        irr = np.irr([-initial_investment] + cash_flows) * 100
        return round(irr, 2)

    def _calculate_irr(self, cash_flows):
        guess_rate = 0.1
        tolerance = 1e-6
        max_iterations = 1000

        def npv(rate):
            return sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))

        for _ in range(max_iterations):
            npv_at_guess = npv(guess_rate)
            npv_prime = sum(-i * cf / (1 + guess_rate) ** (i + 1) for i, cf in enumerate(cash_flows))
            new_guess_rate = guess_rate - npv_at_guess / npv_prime
            if abs(new_guess_rate - guess_rate) < tolerance:
                return guess_rate * 100
            guess_rate = new_guess_rate

        return None

class MarketingEffectiveness(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    time_on_market = models.IntegerField(blank=True, null=True)
    listing_views = models.IntegerField(blank=True, null=True)
    inquiry_to_lease_conversion_rate = models.FloatField(blank=True, null=True)
    date_collected = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def update_metrics(self, time_on_market, listing_views, conversion_rate, date_collected):
        self.time_on_market = time_on_market
        self.listing_views = listing_views
        self.inquiry_to_lease_conversion_rate = conversion_rate
        self.date_collected = date_collected
        self.save()

    def get_marketing_summary(self):
        return {
            "property_id": self.property.property_id,
            "time_on_market": self.time_on_market,
            "listing_views": self.listing_views,
            "conversion_rate": self.inquiry_to_lease_conversion_rate,
            "date_collected": self.date_collected,
        }


