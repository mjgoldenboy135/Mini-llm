from django.urls import path
from .views import AISymptomCheckView, AIAnswerView

urlpatterns = [
    path("symptom/", AISymptomCheckView.as_view(), name="ai_symptom"),
    path("session/<uuid:session_id>/answer/", AIAnswerView.as_view(), name="ai_answer"),
]
