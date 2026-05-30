"""
Добавляет новые реальные IT-компании Ульяновска и стажировки по ним.
Идемпотентен — повторный запуск не создаст дубликатов.

Запуск:
    venv\Scripts\python.exe ulsk_internships\seed_more.py
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ulsk_internships.settings")
django.setup()

from datetime import date
from internships.models import Company, University, Internship

new_companies = [
    {
        "name": "MediaSoft",
        "company_type": "commercial",
        "description": (
            "Ульяновская IT-компания, ~150 сотрудников. Веб- и мобильная разработка, "
            "инженерные системы, заказная разработка для российских и зарубежных клиентов. "
            "Сильная команда frontend/backend и UX."
        ),
        "website": "https://mediasoft.team",
        "contact_email": "hr@mediasoft.team",
        "address": "г. Ульяновск, ул. Карла Маркса, 13А",
        "is_verified": True,
    },
    {
        "name": "ITECH.group",
        "company_type": "commercial",
        "description": (
            "Системный интегратор и разработчик корпоративного ПО. Ульяновск — один "
            "из ключевых центров разработки. Java/Spring, портальные решения, BI, "
            "интеграции с SAP и 1С."
        ),
        "website": "https://itech-group.ru",
        "contact_email": "career@itech-group.ru",
        "address": "г. Ульяновск, ул. Гончарова, 50",
        "is_verified": True,
    },
    {
        "name": "Bell Integrator",
        "company_type": "commercial",
        "description": (
            "Международная IT-компания с центром разработки в Ульяновске. "
            "Заказная разработка для банков, телеком и retail: backend на Java, "
            "тестирование, DevOps, нагрузочное тестирование."
        ),
        "website": "https://bell-integrator.com",
        "contact_email": "ulsk-hr@bell-integrator.com",
        "address": "г. Ульяновск, ул. Можайского, 8/8",
        "is_verified": True,
    },
]

print("=== Компании ===")
for data in new_companies:
    obj, created = Company.objects.get_or_create(name=data["name"], defaults=data)
    print(f"  {'+ создана' if created else '= уже есть'}: {obj.name}")

new_internships = [
    {
        "company_name": "MediaSoft",
        "title": "Frontend-разработчик (React / TypeScript)",
        "field": "frontend",
        "format": "hybrid",
        "duration": "3 месяца",
        "stipend": "30 000 руб/мес",
        "spots": 2,
        "deadline": "2026-08-01",
        "description": (
            "Стажировка в команде frontend MediaSoft. Работа над интерфейсами "
            "b2b-продуктов и проектов для enterprise-заказчиков. Реальные задачи, "
            "менторство опытных разработчиков, понятный план обучения."
        ),
        "requirements": (
            "- Уверенные HTML, CSS, JavaScript\n"
            "- Базовый React и TypeScript\n"
            "- Опыт работы с Git\n"
            "- Студент 3+ курса IT-направления"
        ),
        "tasks": (
            "- Разработка компонентов UI на React\n"
            "- Интеграция с REST API\n"
            "- Покрытие кода тестами (Jest)\n"
            "- Участие в код-ревью и спринт-планировании"
        ),
        "uni_short_names": ["УлГТУ", "УлГУ"],
    },
    {
        "company_name": "ITECH.group",
        "title": "Backend-стажёр (Java / Spring Boot)",
        "field": "backend",
        "format": "office",
        "duration": "4 месяца",
        "stipend": "35 000 руб/мес",
        "spots": 3,
        "deadline": "2026-09-15",
        "description": (
            "Приглашаем студентов в ульяновский офис ITECH.group на позицию "
            "backend-стажёра. Реальные коммерческие проекты для крупных заказчиков, "
            "обучение enterprise-стеку Java/Spring под руководством senior-разработчиков."
        ),
        "requirements": (
            "- Знание Java на базовом уровне\n"
            "- Понимание ООП и базовых алгоритмов\n"
            "- Базовый SQL\n"
            "- Желание расти в enterprise-разработке"
        ),
        "tasks": (
            "- Реализация бизнес-логики на Spring Boot\n"
            "- Работа с PostgreSQL / Oracle\n"
            "- Написание unit- и интеграционных тестов\n"
            "- Участие в проектных митингах и груминге"
        ),
        "uni_short_names": ["УлГТУ", "УлГУ"],
    },
    {
        "company_name": "Bell Integrator",
        "title": "QA-инженер (ручное и автоматизированное тестирование)",
        "field": "qa",
        "format": "remote",
        "duration": "3 месяца",
        "stipend": "25 000 руб/мес",
        "spots": 4,
        "deadline": "2026-07-30",
        "description": (
            "Стажировка в QA-команде Bell Integrator (Ульяновский центр разработки). "
            "Тестирование банковских и телеком-систем. Подходит для тех, кто хочет "
            "начать карьеру в QA с нуля и попробовать переход в автотесты."
        ),
        "requirements": (
            "- Внимательность, аналитический склад ума\n"
            "- Базовое понимание процессов разработки ПО\n"
            "- Английский на чтение тех. документации (B1+)\n"
            "- Студент любого курса IT-направления"
        ),
        "tasks": (
            "- Написание тест-кейсов и чек-листов\n"
            "- Ручное функциональное тестирование\n"
            "- Освоение Postman, JIRA, Selenium\n"
            "- Составление баг-репортов и регрессионных прогонов"
        ),
        "uni_short_names": ["УлГТУ", "УлГУ", "УлГПУ"],
    },
]

print()
print("=== Стажировки ===")
for data in new_internships:
    company = Company.objects.get(name=data.pop("company_name"))
    uni_names = data.pop("uni_short_names")
    deadline_str = data.pop("deadline")
    internship, created = Internship.objects.get_or_create(
        company=company,
        title=data["title"],
        defaults={
            **data,
            "deadline": date.fromisoformat(deadline_str),
            "is_active": True,
        },
    )
    if created:
        unis = University.objects.filter(short_name__in=uni_names)
        internship.university_partnership.set(unis)
    print(f"  {'+ создана' if created else '= уже есть'}: {internship.title} ({company.name})")

print()
print(f"Итого: компаний — {Company.objects.count()}, стажировок — {Internship.objects.count()}")
