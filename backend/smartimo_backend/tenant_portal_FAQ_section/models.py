from django.db import models
from core.models import Category, Feedback
from lease_rental_management.models import Tenant

class FAQ(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)

    def create_faq(self, category_id, question, answer):
        self.category = Category.objects.get(id=category_id)
        self.question = question
        self.answer = answer
        self.save()

    def update_faq(self, question=None, answer=None):
        if question:
            self.question = question
        if answer:
            self.answer = answer
        self.save()

    def delete_faq(self):
        self.delete()

    def get_faq(self):
        return {
            'id': self.id,
            'category': self.category.name,
            'question': self.question,
            'answer': self.answer
        }

class FAQFeedback(Feedback):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('reviewed', 'Reviewed'), ('in-progress', 'In Progress'), ('resolved', 'Resolved')], default='reviewed')

    def create_feedback(self, rating, comments, tenant_id, faq_id, status):
        self.rating = rating,
        self.comments = comments,
        self.tenant = Tenant.objects.get(user_id=tenant_id)
        self.faq = FAQ.objects.get(id=faq_id)
        self.status = status
        self.save()

    def update_feedback(self, status=None):
        if status:
            self.status = status
        self.save()

    def delete_feedback(self):
        self.delete()

    def get_feedback(self):
        return {
            'tenant_id': self.tenant.user_id,
            'faq_id': self.faq.id,
            'status': self.status
        }

class FAQAnalytics(models.Model):
    id = models.AutoField(primary_key=True)
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE)
    page_views = models.PositiveIntegerField(default=0, blank=True, null=True)
    search_queries = models.PositiveIntegerField(default=0, blank=True, null=True)
    average_time_spent = models.FloatField(default=0.0, blank=True, null=True)

    def generate_report(self):
        faqs = FAQ.objects.all()
        report = []
        for faq in faqs:
            analytics = FAQAnalytics.objects.filter(faq_id=faq.id).first()
            if analytics:
                report.append({
                    'faq': faq.id,
                    'page_views': analytics.page_views,
                    'search_queries': analytics.search_queries,
                    'average_time_spent': analytics.average_time_spent
                })
        return report

    def update_analytics(self, faq_id, page_views=None, search_queries=None, average_time_spent=None):
        analytics = FAQAnalytics.objects.filter(faq=faq_id).first()
        if analytics:
            if page_views is not None:
                analytics.page_views = page_views
            if search_queries is not None:
                analytics.search_queries = search_queries
            if average_time_spent is not None:
                analytics.average_time_spent = average_time_spent
            analytics.save()

    def delete_analytics(self):
        self.delete()

    def get_analytics(self):
        return {
            'id': self.id,
            'faq_id': self.faq.id,
            'page_views': self.page_views,
            'search_queries': self.search_queries,
            'average_time_spent': self.average_time_spent
        }

