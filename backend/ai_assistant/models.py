import uuid
from django.db import models
from django.conf import settings


class AISession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    session_key = models.CharField(max_length=64, blank=True)
    symptom = models.CharField(max_length=500)
    # multi-step Q&A stored as list of dicts
    answers = models.JSONField(default=list)
    is_emergency = models.BooleanField(default=False)
    emergency_keywords_matched = models.JSONField(default=list)
    recommended_products = models.ManyToManyField(
        "products.Product", blank=True, related_name="ai_recommendations"
    )
    disclaimer_shown = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"AI Session {self.id} - {self.symptom[:50]}"


EMERGENCY_KEYWORDS = [
    "chest pain",
    "stroke",
    "seizure",
    "difficulty breathing",
    "unconscious",
    "severe bleeding",
    "heart attack",
    "cannot breathe",
    "fainted",
    "overdose",
]

SYMPTOM_QUESTIONS = {
    "headache": [
        {"step": 1, "question": "What is your age group?", "options": ["Child (<12)", "Teenager (12-18)", "Adult (18-60)", "Senior (60+)"]},
        {"step": 2, "question": "How long have you had this headache?", "options": ["Less than 1 hour", "1–6 hours", "6–24 hours", "More than 1 day"]},
        {"step": 3, "question": "Do you have any of these symptoms?", "options": ["Severe/worst headache of life", "Vision problems", "Vomiting", "Fever", "None"], "multi": True},
    ],
    "fever": [
        {"step": 1, "question": "What is your age group?", "options": ["Child (<12)", "Teenager (12-18)", "Adult (18-60)", "Senior (60+)"]},
        {"step": 2, "question": "What is the temperature?", "options": ["Below 38°C", "38–39°C", "39–40°C", "Above 40°C"]},
        {"step": 3, "question": "Additional symptoms?", "options": ["Sore throat", "Rash", "Difficulty breathing", "None"], "multi": True},
    ],
    "cough": [
        {"step": 1, "question": "What is your age group?", "options": ["Child (<12)", "Teenager (12-18)", "Adult (18-60)", "Senior (60+)"]},
        {"step": 2, "question": "How long have you had this cough?", "options": ["Less than 3 days", "3–7 days", "1–2 weeks", "More than 2 weeks"]},
        {"step": 3, "question": "Additional symptoms?", "options": ["Coughing blood", "Difficulty breathing", "Fever", "None"], "multi": True},
    ],
}
