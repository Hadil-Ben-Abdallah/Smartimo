from ninja import Router
from .models import UserFeedback, Survey, Review, FeedbackNotification, Analytics
from .schemas import (
    UserFeedbackSchema, SurveySchema, ReviewSchema, FeedbackNotificationSchema, AnalyticsSchema
)

router = Router()

@router.post("/user-feedback/", response=UserFeedbackSchema)
def create_user_feedback(request, data: UserFeedbackSchema):
    feedback = UserFeedback.objects.create(**data.dict(exclude={'id'}))
    return feedback

@router.get("/user-feedback/{feedback_id}", response=UserFeedbackSchema)
def get_user_feedback(request, feedback_id: int):
    return UserFeedback.objects.get(id=feedback_id)

@router.post("/surveys/", response=SurveySchema)
def create_survey(request, data: SurveySchema):
    survey = Survey.objects.create(**data.dict(exclude={'id'}))
    return survey

@router.get("/surveys/{survey_id}", response=SurveySchema)
def get_survey(request, survey_id: int):
    return Survey.objects.get(id=survey_id)

@router.put("/surveys/{survey_id}", response=SurveySchema)
def update_survey(request, survey_id: int, data: SurveySchema):
    survey = Survey.objects.get(id=survey_id)
    payload = data.dict(exclude_unset=True)
    for key, value in payload.items():
        if key != 'id':
            setattr(survey, key, value)
    survey.save()
    return survey

@router.post("/reviews/", response=ReviewSchema)
def create_review(request, data: ReviewSchema):
    review = Review.objects.create(**data.dict(exclude={'id'}))
    return review

@router.get("/reviews/{review_id}", response=ReviewSchema)
def get_review(request, review_id: int):
    return Review.objects.get(id=review_id)

@router.post("/feedback-notifications/", response=FeedbackNotificationSchema)
def create_feedback_notification(request, data: FeedbackNotificationSchema):
    notification = FeedbackNotification.objects.create(**data.dict(exclude={'id'}))
    return notification

@router.get("/feedback-notifications/{notification_id}", response=FeedbackNotificationSchema)
def get_feedback_notification(request, notification_id: int):
    return FeedbackNotification.objects.get(id=notification_id)

@router.get("/analytics/{analytics_id}", response=AnalyticsSchema)
def get_analytics(request, analytics_id: int):
    return Analytics.objects.get(analytics_id=analytics_id)

@router.post("/analytics/{analytics_id}/feedback-report")
def generate_feedback_report(request, analytics_id: int, criteria: dict):
    analytics = Analytics.objects.get(analytics_id=analytics_id)
    report = analytics.generate_feedback_report(criteria)
    return report

@router.post("/analytics/{analytics_id}/survey-report")
def generate_survey_report(request, analytics_id: int, criteria: dict):
    analytics = Analytics.objects.get(analytics_id=analytics_id)
    report = analytics.generate_survey_report(criteria)
    return report

@router.post("/analytics/{analytics_id}/review-report")
def generate_review_report(request, analytics_id: int, criteria: dict):
    analytics = Analytics.objects.get(analytics_id=analytics_id)
    report = analytics.generate_review_report(criteria)
    return report

@router.post("/analytics/{analytics_id}/identify-trends")
def identify_trends(request, analytics_id: int, data: dict):
    analytics = Analytics.objects.get(analytics_id=analytics_id)
    trends = analytics.identify_trends(data)
    return trends

