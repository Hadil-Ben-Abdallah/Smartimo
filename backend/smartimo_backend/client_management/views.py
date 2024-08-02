from ninja import Router
from typing import List
from .models import Client, Interaction, Reminder, ClientAnalytics, ClientRealEstateAgent
from .schemas import ClientSchema, InteractionSchema, ReminderSchema, ClientAnalyticsSchema

router = Router()

@router.post("/add-client", response=ClientSchema)
def add_client(request, data: ClientSchema):
    client_data = data.dict(exclude={'id'})
    client_instance = Client.objects.create(**client_data)
    return client_instance

@router.put("/update-client/{client_id}", response=ClientSchema)
def update_client(request, client_id: int, data: ClientSchema):
    client_instance = Client.objects.get(id=client_id)
    for key, value in data.dict().items():
        setattr(client_instance, key, value)
    client_instance.save()
    return client_instance

@router.delete("/delete-client/{client_id}")
def delete_client(request, client_id: int):
    client_instance = Client.objects.get(id=client_id)
    client_instance.delete()
    return {"success": True}

@router.get("/get-client/{client_id}", response=ClientSchema)
def get_client(request, client_id: int):
    client_instance = Client.objects.get(id=client_id)
    return client_instance

@router.post("/log-interaction", response=InteractionSchema)
def log_interaction(request, data: InteractionSchema):
    interaction_data = data.dict(exclude={'id'})
    interaction_instance = Interaction.objects.create(**interaction_data)
    return interaction_instance

@router.get("/get-interactions/{client_id}", response=List[InteractionSchema])
def get_interactions(request, client_id: int):
    interactions = Interaction.objects.filter(client_id=client_id)
    return list(interactions)

@router.post("/set-reminder", response=ReminderSchema)
def set_reminder(request, data: ReminderSchema):
    reminder_data = data.dict(exclude={'id'})
    reminder_instance = Reminder.objects.create(**reminder_data)
    return reminder_instance

@router.put("/update-reminder/{reminder_id}", response=ReminderSchema)
def update_reminder(request, reminder_id: int, data: ReminderSchema):
    reminder_instance = Reminder.objects.get(id=reminder_id)
    for key, value in data.dict().items():
        setattr(reminder_instance, key, value)
    reminder_instance.save()
    return reminder_instance

@router.delete("/delete-reminder/{reminder_id}")
def delete_reminder(request, reminder_id: int):
    reminder_instance = Reminder.objects.get(id=reminder_id)
    reminder_instance.delete()
    return {"success": True}

@router.get("/get-reminders/{client_id}", response=List[ReminderSchema])
def get_reminders(request, client_id: int):
    reminders = Reminder.objects.filter(client_id=client_id)
    return list(reminders)

@router.get("/generate-report/{client_id}", response=ClientAnalyticsSchema)
def generate_report(request, client_id: int):
    analytics = ClientAnalytics.objects.get(client_id=client_id)
    return analytics.generate_report()

@router.get("/view-clients/{agent_id}", response=List[ClientSchema])
def view_clients(request, agent_id: int):
    agent = ClientRealEstateAgent.objects.get(id=agent_id)
    return agent.view_clients()

@router.post("/assign-tag/{client_id}/{tag}", response=ClientSchema)
def assign_tag(request, client_id: int, tag: str):
    client = Client.objects.get(id=client_id)
    agent = ClientRealEstateAgent.objects.get(id=client.agent_id)
    agent.assign_tag(client, tag)
    return client

@router.get("/filter-clients/{agent_id}/{tag}", response=List[ClientSchema])
def filter_clients(request, agent_id: int, tag: str):
    agent = ClientRealEstateAgent.objects.get(id=agent_id)
    return agent.filter_clients(tag)
