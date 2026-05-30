"""
Скрипт для загрузки начальных данных об IT-компаниях и вузах Ульяновска.
Запуск: python manage.py shell < internships/management/commands/seed_data.py
Или: python manage.py seed
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ulsk_internships.settings')
django.setup()

from internships.models import University, Company, Internship

# Universities
universities_data = [
    {
        "id": 1, "name": "Ульяновский государственный технический университет",
        "short_name": "УлГТУ", "website": "https://ulstu.ru",
        "description": "Крупнейший технический вуз Ульяновска. Готовит специалистов в области ИТ, автоматизации, радиотехники и связи.",
        "it_directions": "Информатика и ВТ, Программная инженерия, Информационная безопасность, Прикладная математика и информатика, Автоматизация ТП, Радиотехника, Инфокоммуникационные технологии"
    },
    {
        "id": 2, "name": "Ульяновский государственный университет",
        "short_name": "УлГУ", "website": "https://ulsu.ru",
        "description": "Классический университет с развитыми IT-направлениями. Математический факультет и факультет информационных технологий.",
        "it_directions": "Прикладная математика и информатика, Информационные системы и технологии, Компьютерные науки, Математика и компьютерные науки"
    },
    {
        "id": 3, "name": "Ульяновский государственный педагогический университет им. И.Н. Ульянова",
        "short_name": "УлГПУ", "website": "https://ulspu.ru",
        "description": "Педагогический университет с направлениями информатики и цифровых технологий в образовании.",
        "it_directions": "Педагогическое образование (Информатика), Математика и информатика, Прикладная информатика"
    },
    {
        "id": 4, "name": "Ульяновское высшее авиационное училище гражданской авиации",
        "short_name": "УВАУГА", "website": "https://uvauga.ru",
        "description": "Авиационный институт, готовящий специалистов в том числе в области IT для авиации.",
        "it_directions": "Информационные системы и технологии (авиация), Автоматизация и управление"
    },
    {
        "id": 5, "name": "Ульяновский институт гражданской авиации им. Б.П. Бугаева",
        "short_name": "УИ ГА", "website": "https://uiga.ru",
        "description": "Специализированный институт ГА с IT-направлениями для авиационной отрасли.",
        "it_directions": "Информационные технологии на воздушном транспорте, Системы автоматизации и управления"
    },
]

for data in universities_data:
    uni, created = University.objects.update_or_create(
        pk=data["id"],
        defaults={k: v for k, v in data.items() if k != "id"}
    )
    print(f"{'Создан' if created else 'Обновлён'}: {uni.short_name}")

# Companies
companies_data = [
    {
        "id": 1, "name": "Контек-Софт", "company_type": "commercial", "university_id": None,
        "description": "Один из крупнейших IT-работодателей Ульяновска. Разрабатывает промышленное ПО, ERP/MES-системы для машиностроения и авиации.",
        "website": "https://kontek.ru", "contact_email": "hr@kontek.ru", "address": "г. Ульяновск", "is_verified": True
    },
    {
        "id": 2, "name": "Simbirsoft", "company_type": "commercial", "university_id": None,
        "description": "Крупная аутсорсинговая IT-компания. Топ-30 крупнейших IT-компаний России. Web, Mobile, QA, Data Science.",
        "website": "https://simbirsoft.com", "contact_email": "career@simbirsoft.com",
        "address": "г. Ульяновск, ул. Гончарова, 36", "is_verified": True
    },
    {
        "id": 3, "name": "АйТи Ульяновск (IT72)", "company_type": "commercial", "university_id": None,
        "description": "Региональная IT-компания. Веб-разработка, мобильные приложения, цифровая трансформация бизнеса.",
        "website": "", "contact_email": "", "address": "г. Ульяновск", "is_verified": True
    },
    {
        "id": 4, "name": "Научно-образовательный центр УлГТУ", "company_type": "university", "university_id": 1,
        "description": "Структурное подразделение УлГТУ. Прикладные исследования в области встраиваемых систем, САПР и промышленной автоматизации.",
        "website": "https://ulstu.ru", "contact_email": "noc@ulstu.ru",
        "address": "г. Ульяновск, ул. Северный Венец, 32", "is_verified": True
    },
    {
        "id": 5, "name": "Центр инновационного развития УлГУ", "company_type": "university", "university_id": 2,
        "description": "Инновационное подразделение УлГУ. Проекты в области Data Science, AI и веб-технологий совместно со студентами.",
        "website": "https://ulsu.ru", "contact_email": "innovation@ulsu.ru",
        "address": "г. Ульяновск, ул. Льва Толстого, 42", "is_verified": True
    },
    {
        "id": 6, "name": "Корпорация развития Ульяновской области", "company_type": "government", "university_id": None,
        "description": "Государственная структура, курирующая IT-кластер Ульяновска. Стажировки в IT-компаниях региона.",
        "website": "https://ulkorporacia.ru", "contact_email": "it@ulkorporacia.ru",
        "address": "г. Ульяновск, ул. Спасская, 5", "is_verified": True
    },
    {
        "id": 7, "name": "IT-стартапы (резиденты Ульяновска)", "company_type": "startup", "university_id": None,
        "description": "Стартапы в области fintech, edtech, logtech с офисами в Ульяновске.",
        "website": "", "contact_email": "", "address": "г. Ульяновск", "is_verified": True
    },
    {
        "id": 8, "name": "НПО «Марс»", "company_type": "commercial", "university_id": 1,
        "description": "Оборонно-промышленное предприятие Ульяновска. Встраиваемое ПО и навигационные системы для ВМФ.",
        "website": "https://npomars.com", "contact_email": "hr@npomars.com",
        "address": "г. Ульяновск, ул. Марса, 1", "is_verified": True
    },
]

for data in companies_data:
    company, created = Company.objects.update_or_create(
        pk=data["id"],
        defaults={k: v for k, v in data.items() if k != "id"}
    )
    print(f"{'Создана' if created else 'Обновлена'}: {company.name}")

# Internships
internships_data = [
    {
        "company_id": 2, "title": "Backend-разработчик (Python/Django)",
        "field": "backend", "format": "hybrid", "duration": "3 месяца", "stipend": "25 000 руб/мес",
        "spots": 3, "is_active": True, "deadline": "2025-08-01",
        "description": "Приглашаем студентов на стажировку в команду backend-разработки. Работа над реальными коммерческими проектами под руководством опытных разработчиков.\n\nSimbirsoft входит в топ-30 крупнейших IT-компаний России.",
        "requirements": "- Знание Python на базовом/среднем уровне\n- Понимание основ веб-разработки (HTTP, REST API)\n- Базовые знания SQL\n- Желание учиться",
        "tasks": "- Разработка REST API на Django/DRF\n- Написание unit-тестов\n- Участие в код-ревью\n- Работа с PostgreSQL",
        "uni_ids": [1, 2]
    },
    {
        "company_id": 2, "title": "Frontend-разработчик (React)",
        "field": "frontend", "format": "office", "duration": "2-3 месяца", "stipend": "20 000 руб/мес",
        "spots": 2, "is_active": True, "deadline": "2025-07-15",
        "description": "Стажировка в команде frontend-разработки. Работа над современными веб-интерфейсами для крупных российских заказчиков.",
        "requirements": "- Знание HTML/CSS, JavaScript\n- Базовое знание React\n- Понимание адаптивной вёрстки\n- Опыт с Git",
        "tasks": "- Вёрстка компонентов на React\n- Интеграция с backend API\n- Участие в проектировании UI/UX",
        "uni_ids": [1, 2, 3]
    },
    {
        "company_id": 1, "title": "Разработчик встраиваемых систем (C/C++)",
        "field": "backend", "format": "office", "duration": "Лето 2025 (июнь-август)", "stipend": "30 000 руб/мес",
        "spots": 2, "is_active": True, "deadline": "2025-06-01",
        "description": "Стажировка в команде разработки промышленного ПО для машиностроительных предприятий. Контек-Софт — лидер в разработке MES-систем для промышленности России.",
        "requirements": "- Знание C/C++ на базовом уровне\n- Понимание принципов ООП\n- Желательно: опыт с микроконтроллерами\n- Студент 3-4 курса УлГТУ",
        "tasks": "- Разработка драйверов для промышленных контроллеров\n- Тестирование и отладка ПО\n- Работа с технической документацией",
        "uni_ids": [1]
    },
    {
        "company_id": 5, "title": "Data Science / ML стажёр",
        "field": "data", "format": "hybrid", "duration": "4 месяца", "stipend": "15 000 руб/мес",
        "spots": 3, "is_active": True, "deadline": "2025-09-01",
        "description": "Стажировка в Центре инновационного развития УлГУ. Работа над исследовательскими проектами в области машинного обучения.",
        "requirements": "- Знание Python (pandas, numpy, sklearn)\n- Базовые знания математической статистики\n- Студент 3+ курса",
        "tasks": "- Сбор и обработка данных\n- Построение и обучение ML-моделей\n- Визуализация результатов",
        "uni_ids": [2, 1]
    },
    {
        "company_id": 4, "title": "Инженер по тестированию ПО (QA)",
        "field": "qa", "format": "office", "duration": "3 месяца", "stipend": "Не оплачивается (зачёт практики)",
        "spots": 4, "is_active": True, "deadline": "2025-08-15",
        "description": "Стажировка в НОЦ УлГТУ по тестированию программного обеспечения. Участие в реальных проектах для промышленных предприятий.",
        "requirements": "- Базовое понимание процессов разработки ПО\n- Внимательность и аналитическое мышление\n- Студент любого курса IT-специальности",
        "tasks": "- Ручное тестирование ПО\n- Составление тест-кейсов и баг-репортов\n- Освоение инструментов автотестирования",
        "uni_ids": [1, 2, 3]
    },
    {
        "company_id": 8, "title": "Разработчик навигационных систем (Python/C++)",
        "field": "backend", "format": "office", "duration": "6 месяцев", "stipend": "35 000 руб/мес",
        "spots": 2, "is_active": True, "deadline": "2025-07-01",
        "description": "НПО «Марс» приглашает студентов на стажировку в отдел разработки ПО для навигационных и управляющих систем.",
        "requirements": "- Гражданство РФ (обязательно)\n- Знание Python или C++\n- Базовые знания алгоритмов\n- Студент 3-5 курса УлГТУ",
        "tasks": "- Разработка алгоритмов обработки сигналов\n- Тестирование и верификация ПО\n- Работа с документацией по ГОСТ",
        "uni_ids": [1]
    },
    {
        "company_id": 2, "title": "Мобильный разработчик (Android / Kotlin)",
        "field": "mobile", "format": "office", "duration": "3 месяца", "stipend": "22 000 руб/мес",
        "spots": 2, "is_active": True, "deadline": "2025-08-20",
        "description": "Стажировка в команде мобильной разработки Simbirsoft. Работа над Android-приложениями для клиентов из банковской и retail-сферы.",
        "requirements": "- Знание Kotlin или Java\n- Базовое понимание Android SDK\n- Желание развиваться в мобильной разработке",
        "tasks": "- Разработка UI компонентов\n- Интеграция с REST API\n- Написание unit-тестов",
        "uni_ids": [1, 2]
    },
    {
        "company_id": 5, "title": "Веб-разработчик (Django + Vue.js)",
        "field": "fullstack", "format": "remote", "duration": "3 месяца", "stipend": "18 000 руб/мес",
        "spots": 2, "is_active": True, "deadline": "2025-09-15",
        "description": "Удалённая стажировка в ЦИР УлГУ. Разработка образовательных веб-платформ для университета.",
        "requirements": "- Знание Python/Django или Vue.js\n- Базовое знание HTML/CSS\n- Студент 2+ курса",
        "tasks": "- Разработка функционала веб-приложения\n- Работа с базами данных\n- Тестирование и документирование",
        "uni_ids": [2, 1, 3]
    },
]

from datetime import date
for data in internships_data:
    uni_ids = data.pop("uni_ids")
    deadline_str = data.pop("deadline", None)
    internship = Internship.objects.create(
        **data,
        deadline=date.fromisoformat(deadline_str) if deadline_str else None
    )
    internship.university_partnership.set(uni_ids)
    print(f"Создана стажировка: {internship.title}")

print("\n✅ Данные успешно загружены!")
print(f"Вузов: {University.objects.count()}")
print(f"Компаний: {Company.objects.count()}")
print(f"Стажировок: {Internship.objects.count()}")
