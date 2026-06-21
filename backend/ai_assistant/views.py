from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import AISession, EMERGENCY_KEYWORDS, SYMPTOM_QUESTIONS
from products.models import Product

SYMPTOM_PRODUCT_MAP = {
    "headache": ["Panadol", "Adol", "Fevadol", "Brufen"],
    "fever": ["Panadol", "Adol", "Fevadol", "Ibuprofen"],
    "cough": ["Actifed", "Robitussin", "Codiclear"],
    "cold": ["Actifed", "Coldact", "Cetirizine"],
    "allergy": ["Cetirizine", "Clarityne", "Loratadine"],
    "stomach": ["Omeprazole", "Gaviscon", "Buscopan"],
    "diarrhea": ["Smecta", "Imodium", "Flagyl"],
    "nausea": ["Motilium", "Stemetil", "Ondansetron"],
}

EMERGENCY_RESPONSE = {
    "is_emergency": True,
    "title": "Medical Emergency",
    "message": (
        "Seek immediate medical attention.\n\n"
        "Go to nearest hospital or emergency department.\n\n"
        "If unable to reach medical care immediately, contact local emergency services "
        "or a qualified healthcare professional urgently."
    ),
    "recommended_products": [],
    "disclaimer": None,
}

DISCLAIMER = (
    "AI is not a doctor. The information provided is for general guidance only. "
    "Doctor's advice is final. Always consult a qualified healthcare professional."
)


def detect_emergency(text: str) -> list[str]:
    text_lower = text.lower()
    return [kw for kw in EMERGENCY_KEYWORDS if kw in text_lower]


class AISymptomCheckView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        symptom = request.data.get("symptom", "").strip()
        if not symptom:
            return Response({"detail": "Symptom is required."}, status=400)

        # Emergency detection
        matched = detect_emergency(symptom)
        if matched:
            return Response(EMERGENCY_RESPONSE)

        # Determine questions for this symptom
        symptom_key = None
        for key in SYMPTOM_QUESTIONS:
            if key in symptom.lower():
                symptom_key = key
                break

        questions = SYMPTOM_QUESTIONS.get(symptom_key, [
            {"step": 1, "question": "What is your age group?", "options": ["Child (<12)", "Teenager (12-18)", "Adult (18-60)", "Senior (60+)"]},
            {"step": 2, "question": "How long have you had this symptom?", "options": ["Less than 1 day", "1–3 days", "4–7 days", "More than 1 week"]},
            {"step": 3, "question": "Do you have any of these additional symptoms?", "options": ["Difficulty breathing", "High fever", "Severe pain", "None"], "multi": True},
        ])

        session = AISession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            symptom=symptom,
        )

        return Response({
            "session_id": str(session.id),
            "symptom": symptom,
            "is_emergency": False,
            "questions": questions,
        })


class AIAnswerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, session_id):
        try:
            session = AISession.objects.get(id=session_id)
        except AISession.DoesNotExist:
            return Response({"detail": "Session not found."}, status=404)

        answers = request.data.get("answers", [])
        session.answers = answers
        session.save()

        # Check emergency in answers
        all_text = " ".join(str(a) for a in answers) + " " + session.symptom
        matched = detect_emergency(all_text)
        if matched:
            session.is_emergency = True
            session.emergency_keywords_matched = matched
            session.save()
            return Response(EMERGENCY_RESPONSE)

        # Recommend products
        symptom_key = None
        for key in SYMPTOM_PRODUCT_MAP:
            if key in session.symptom.lower():
                symptom_key = key
                break

        product_names = SYMPTOM_PRODUCT_MAP.get(symptom_key, [])
        products = Product.objects.filter(
            name__in=product_names, is_active=True, prescription_required=False
        )[:5]

        session.recommended_products.set(products)
        session.disclaimer_shown = True
        session.save()

        from products.serializers import ProductListSerializer
        return Response({
            "session_id": str(session.id),
            "is_emergency": False,
            "disclaimer": DISCLAIMER,
            "recommended_products": ProductListSerializer(products, many=True).data,
            "advice": "Based on your symptoms, these OTC products may help. Consult a pharmacist or doctor if symptoms persist.",
        })
