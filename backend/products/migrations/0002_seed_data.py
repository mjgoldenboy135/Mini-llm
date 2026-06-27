from django.db import migrations
import uuid


CATEGORIES = [
    {"name": "Pain Relief",       "name_ar": "مسكنات الألم",       "slug": "pain-relief"},
    {"name": "Fever",             "name_ar": "خافض الحرارة",        "slug": "fever"},
    {"name": "Cold & Flu",        "name_ar": "نزلات البرد والأنفلونزا", "slug": "cold-flu"},
    {"name": "Digestive Health",  "name_ar": "صحة الجهاز الهضمي",  "slug": "digestive-health"},
    {"name": "Allergy",           "name_ar": "الحساسية",             "slug": "allergy"},
    {"name": "Vitamins",          "name_ar": "الفيتامينات",          "slug": "vitamins"},
    {"name": "First Aid",         "name_ar": "الإسعافات الأولية",   "slug": "first-aid"},
    {"name": "Skin Care",         "name_ar": "العناية بالبشرة",     "slug": "skin-care"},
]

PRODUCTS = [
    # Pain Relief / Fever
    {"sku": "PANA-500",  "name": "Panadol",      "name_ar": "بنادول",     "generic_name": "Paracetamol 500mg",  "brand": "GSK",      "category_slug": "pain-relief",     "price": "12.00",  "stock": 200, "dosage_form": "Tablet",  "strength": "500mg",  "prescription_required": False, "description": "Paracetamol 500mg for pain and fever relief."},
    {"sku": "ADOL-250",  "name": "Adol",         "name_ar": "أدول",       "generic_name": "Paracetamol 250mg",  "brand": "Julphar",  "category_slug": "fever",           "price": "8.00",   "stock": 150, "dosage_form": "Syrup",   "strength": "250mg",  "prescription_required": False, "description": "Paracetamol syrup suitable for children."},
    {"sku": "FEVA-500",  "name": "Fevadol",      "name_ar": "فيفادول",    "generic_name": "Paracetamol 500mg",  "brand": "Tabuk",    "category_slug": "fever",           "price": "10.00",  "stock": 180, "dosage_form": "Tablet",  "strength": "500mg",  "prescription_required": False, "description": "Fast-acting paracetamol for fever and mild pain."},
    {"sku": "IBUP-400",  "name": "Brufen",       "name_ar": "بروفين",     "generic_name": "Ibuprofen 400mg",    "brand": "Abbott",   "category_slug": "pain-relief",     "price": "15.00",  "stock": 160, "dosage_form": "Tablet",  "strength": "400mg",  "prescription_required": False, "description": "Ibuprofen anti-inflammatory for pain and inflammation."},
    {"sku": "IBUP-200",  "name": "Ibuprofen",    "name_ar": "إيبوبروفين",  "generic_name": "Ibuprofen 200mg",    "brand": "Generic",  "category_slug": "pain-relief",     "price": "9.00",   "stock": 140, "dosage_form": "Tablet",  "strength": "200mg",  "prescription_required": False, "description": "Standard ibuprofen for mild to moderate pain."},
    # Cough / Cold
    {"sku": "ACTI-TAB",  "name": "Actifed",      "name_ar": "أكتيفيد",    "generic_name": "Triprolidine + Pseudoephedrine", "brand": "GSK", "category_slug": "cold-flu",   "price": "18.00",  "stock": 120, "dosage_form": "Tablet",  "strength": "2.5/60mg", "prescription_required": False, "description": "Relief from cold, flu and nasal congestion."},
    {"sku": "ROBI-100",  "name": "Robitussin",   "name_ar": "روبيتوسين",  "generic_name": "Dextromethorphan 15mg", "brand": "Pfizer",  "category_slug": "cold-flu",       "price": "22.00",  "stock": 100, "dosage_form": "Syrup",   "strength": "15mg/5ml", "prescription_required": False, "description": "Cough suppressant syrup for dry cough."},
    {"sku": "COLD-CAP",  "name": "Coldact",      "name_ar": "كولداكت",    "generic_name": "Chlorphenamine + Paracetamol", "brand": "Eva",  "category_slug": "cold-flu",     "price": "14.00",  "stock": 110, "dosage_form": "Capsule", "strength": "500mg",  "prescription_required": False, "description": "All-in-one cold and flu relief capsule."},
    # Allergy
    {"sku": "CETI-10",   "name": "Cetirizine",   "name_ar": "سيتيريزين",  "generic_name": "Cetirizine 10mg",    "brand": "Generic",  "category_slug": "allergy",         "price": "11.00",  "stock": 130, "dosage_form": "Tablet",  "strength": "10mg",   "prescription_required": False, "description": "Non-drowsy antihistamine for allergies."},
    {"sku": "CLAR-10",   "name": "Clarityne",    "name_ar": "كلاريتين",   "generic_name": "Loratadine 10mg",    "brand": "Bayer",    "category_slug": "allergy",         "price": "25.00",  "stock": 90,  "dosage_form": "Tablet",  "strength": "10mg",   "prescription_required": False, "description": "24-hour non-drowsy allergy relief."},
    {"sku": "LORA-10",   "name": "Loratadine",   "name_ar": "لوراتادين",  "generic_name": "Loratadine 10mg",    "brand": "Generic",  "category_slug": "allergy",         "price": "8.50",   "stock": 120, "dosage_form": "Tablet",  "strength": "10mg",   "prescription_required": False, "description": "Generic loratadine for hay fever and hives."},
    # Digestive
    {"sku": "OMEP-20",   "name": "Omeprazole",   "name_ar": "أوميبرازول", "generic_name": "Omeprazole 20mg",    "brand": "Generic",  "category_slug": "digestive-health","price": "20.00",  "stock": 100, "dosage_form": "Capsule", "strength": "20mg",   "prescription_required": False, "description": "Proton pump inhibitor for acid reflux and heartburn."},
    {"sku": "GAVI-LIQ",  "name": "Gaviscon",     "name_ar": "جافيسكون",   "generic_name": "Alginate antacid",   "brand": "RB",       "category_slug": "digestive-health","price": "28.00",  "stock": 80,  "dosage_form": "Liquid",  "strength": "500mg",  "prescription_required": False, "description": "Fast relief from heartburn and acid indigestion."},
    {"sku": "BUSC-10",   "name": "Buscopan",     "name_ar": "بوسكوبان",   "generic_name": "Hyoscine butylbromide 10mg", "brand": "Sanofi", "category_slug": "digestive-health","price": "16.00","stock": 95,  "dosage_form": "Tablet",  "strength": "10mg",   "prescription_required": False, "description": "Relieves stomach cramps and spasms."},
    {"sku": "SMEC-3G",   "name": "Smecta",       "name_ar": "سميكتا",     "generic_name": "Diosmectite 3g",     "brand": "Ipsen",    "category_slug": "digestive-health","price": "35.00",  "stock": 70,  "dosage_form": "Powder",  "strength": "3g",     "prescription_required": False, "description": "Natural clay for diarrhea and bowel irritation."},
    {"sku": "IMOD-2",    "name": "Imodium",      "name_ar": "إيموديوم",   "generic_name": "Loperamide 2mg",     "brand": "J&J",      "category_slug": "digestive-health","price": "19.00",  "stock": 85,  "dosage_form": "Capsule", "strength": "2mg",    "prescription_required": False, "description": "Fast relief from acute diarrhea."},
    # Nausea
    {"sku": "MOTI-10",   "name": "Motilium",     "name_ar": "موتيليوم",   "generic_name": "Domperidone 10mg",   "brand": "J&J",      "category_slug": "digestive-health","price": "24.00",  "stock": 75,  "dosage_form": "Tablet",  "strength": "10mg",   "prescription_required": False, "description": "Anti-nausea and promotes gastric motility."},
    # Vitamins
    {"sku": "VITC-500",  "name": "Vitamin C",    "name_ar": "فيتامين سي", "generic_name": "Ascorbic Acid 500mg","brand": "Generic",  "category_slug": "vitamins",        "price": "15.00",  "stock": 200, "dosage_form": "Tablet",  "strength": "500mg",  "prescription_required": False, "description": "Vitamin C for immune support."},
    {"sku": "VITD-1K",   "name": "Vitamin D3",   "name_ar": "فيتامين د",  "generic_name": "Cholecalciferol 1000IU","brand":"Generic","category_slug": "vitamins",       "price": "30.00",  "stock": 160, "dosage_form": "Tablet",  "strength": "1000 IU","prescription_required": False, "description": "Vitamin D3 for bone health and immunity."},
    {"sku": "ZINC-10",   "name": "Zinc",         "name_ar": "زنك",        "generic_name": "Zinc Gluconate 10mg","brand": "Generic",  "category_slug": "vitamins",        "price": "12.00",  "stock": 140, "dosage_form": "Tablet",  "strength": "10mg",   "prescription_required": False, "description": "Zinc supplement for immune function."},
]


def seed(apps, schema_editor):
    Category = apps.get_model("products", "Category")
    Product = apps.get_model("products", "Product")

    cat_map = {}
    for c in CATEGORIES:
        obj, _ = Category.objects.get_or_create(
            slug=c["slug"],
            defaults={"id": uuid.uuid4(), "name": c["name"], "name_ar": c["name_ar"]},
        )
        cat_map[c["slug"]] = obj

    for p in PRODUCTS:
        Product.objects.get_or_create(
            sku=p["sku"],
            defaults={
                "id": uuid.uuid4(),
                "name": p["name"],
                "name_ar": p["name_ar"],
                "generic_name": p["generic_name"],
                "brand": p["brand"],
                "category": cat_map[p["category_slug"]],
                "price": p["price"],
                "stock": p["stock"],
                "dosage_form": p["dosage_form"],
                "strength": p["strength"],
                "prescription_required": p["prescription_required"],
                "description": p["description"],
                "is_active": True,
            },
        )


def unseed(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    Category = apps.get_model("products", "Category")
    Product.objects.filter(sku__in=[p["sku"] for p in PRODUCTS]).delete()
    Category.objects.filter(slug__in=[c["slug"] for c in CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
