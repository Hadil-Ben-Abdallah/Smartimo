from django.db import models
from lease_rental_management.models import Tenant, PropertyManager

class Chatbot(models.Model):
    id = models.AutoField(primary_key=True)
    training_data = models.JSONField(blank=True, null=True)
    interaction_history = models.JSONField(blank=True, null=True)
    escalation_protocols = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive')

    def train_bot(self, new_data):
        self.training_data += new_data
        self.save()

    def respond_to_query(self, query):
        for faq in self.training_data:
            if faq['question'].lower() in query.lower():
                return faq['answer']
        return "I'm sorry, I don't have an answer for that."

    def perform_task(self, tenant_id, task_type, task_data):
        task = ChatbotTask.objects.create(
            chatbot=self.id,
            tenant=tenant_id,
            task_type=task_type,
            task_data=task_data,
            status='pending'
        )
        return task

    def escalate_issue(self, interaction_id, tenant_id, issue_details):
        property_manager = PropertyManager.objects.first()
        escalation = Escalation.objects.create(
            interaction=interaction_id,
            tenant=tenant_id,
            property_manager=property_manager.user_id,
            issue_details=issue_details,
            status='pending'
        )
        escalation.notify_manager()
        return escalation


class ChatbotInteraction(models.Model):
    id = models.AutoField(primary_key=True)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    query = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('resolved', 'Resolved'), ('escalated', 'Escalated')], default='resolved')

    def log_interaction(self):
        interaction_log = {
            "tenant_id": self.tenant.user_id,
            "query": self.query,
            "response": self.response,
            "status": self.status,
        }
        chatbot = self.chatbot.id
        Chatbot.interaction_history.append(interaction_log)
        chatbot.save()

    def retrieve_history(self):
        return ChatbotInteraction.objects.filter(tenant=self.tenant.user_id)

    def analyze_interaction(self):
        escalation_keywords = ['complaint', 'issue', 'problem']
        if any(keyword in self.query.lower() for keyword in escalation_keywords):
            return 'Potential Escalation'
        return 'Normal'


class ChatbotTask(models.Model):
    id = models.AutoField(primary_key=True)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=50, blank=True, null=True)
    task_data = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')

    def initiate_task(self):
        self.status = 'pending'
        self.save()

    def complete_task(self):
        self.status = 'completed'
        self.save()

    def confirm_task(self):
        if self.status == 'pending':
            self.status = 'awaiting confirmation'
            self.save()
            return "Please confirm the completion of this task."
        return "Task is not ready for confirmation."


class Escalation(models.Model):
    id = models.AutoField(primary_key=True)
    interaction = models.ForeignKey(ChatbotInteraction, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property_manager = models.ForeignKey(PropertyManager, on_delete=models.CASCADE)
    issue_details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    def notify_manager(self):
        manager = self.property_manager
        print(f"Notification sent to {manager.username}: Escalated Issue - {self.issue_details}")

    def track_resolution(self):
        return self.status

    def provide_context(self):
        interaction = self.interaction
        return {
            "tenant": self.tenant.username,
            "interaction": interaction.query,
            "response": interaction.response,
            "issue_details": self.issue_details,
        }


class ChatbotAnalytics(models.Model):
    id = models.AutoField(primary_key=True)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    usage_metrics = models.JSONField(blank=True, null=True)
    user_feedback = models.JSONField(blank=True, null=True)
    performance_insights = models.JSONField(blank=True, null=True)
    trending_topics = models.JSONField(blank=True, null=True)

    def generate_report(self):
        report = {
            "total_interactions": len(self.usage_metrics),
            "average_response_time": self.performance_insights.get("average_response_time"),
            "trending_topics": self.trending_topics,
        }
        return report

    def analyze_trends(self):
        trending = {}
        for interaction in self.usage_metrics:
            query = interaction['query'].lower()
            if query in trending:
                trending[query] += 1
            else:
                trending[query] = 1
        return trending

    def recommend_improvements(self):
        recommendations = []
        if self.performance_insights.get("average_response_time") > 5:
            recommendations.append("Improve response time by optimizing query handling.")
        
        covered_topics = {topic['question'].lower() for topic in self.chatbot.training_data}
        uncovered_topics = [topic for topic in self.trending_topics if topic.lower() not in covered_topics]
        
        if uncovered_topics:
            recommendations.append("Update training data to cover new trending topics: " + ", ".join(uncovered_topics))
        
        return recommendations


class ChatbotCustomization(models.Model):
    id = models.AutoField(primary_key=True)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    custom_flows = models.JSONField(blank=True, null=True)
    integration_settings = models.JSONField(blank=True, null=True)
    custom_responses = models.JSONField(blank=True, null=True)

    def add_custom_flow(self, flow_data):
        self.custom_flows.append(flow_data)
        self.save()

    def integrate_system(self, system_settings):
        self.integration_settings.update(system_settings)
        self.save()

    def update_responses(self, response_data):
        self.custom_responses.update(response_data)
        self.save()

