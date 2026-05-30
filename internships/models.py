# =============================================================
#  models.py — описание таблиц базы данных (модели Django)
# =============================================================
#  Каждый класс, наследующий models.Model, превращается Django ORM
#  в отдельную таблицу базы данных. Django сам создаёт SQL-команды
#  и хранит их в файлах migrations/. Когда мы запускаем
#  `python manage.py migrate`, Django применяет миграции и создаёт
#  таблицы в PostgreSQL.
# =============================================================

from django.db import models                       # базовый класс Model и типы полей
from django.contrib.auth.models import User        # встроенная модель пользователя Django


# -------------------------------------------------------------
#  Модель «Университет» — справочник вузов Ульяновска
# -------------------------------------------------------------
class University(models.Model):
    # CharField — короткое текстовое поле (varchar в БД), max_length обязателен
    name = models.CharField("Название вуза", max_length=255)
    # Аббревиатура: УлГТУ, УлГУ и т.д.
    short_name = models.CharField("Аббревиатура", max_length=50)
    # URLField — то же, что CharField, но с проверкой формата URL
    website = models.URLField("Сайт вуза", blank=True)  # blank=True — поле необязательно в формах
    # TextField — большое текстовое поле (text в БД), без ограничения длины
    description = models.TextField("Описание", blank=True)
    it_directions = models.TextField("IT направления", blank=True)
    # ImageField — поле для изображения; upload_to — папка внутри media/
    # null=True означает, что в БД допустимо NULL (фото может отсутствовать)
    logo = models.ImageField("Логотип", upload_to="universities/", blank=True, null=True)

    # Вложенный класс Meta настраивает поведение модели в Django
    class Meta:
        verbose_name = "Вуз"                  # как называется одна запись в админке
        verbose_name_plural = "Вузы"          # как называется список записей
        ordering = ["short_name"]             # сортировка по умолчанию (по аббревиатуре А–Я)

    # __str__ возвращает строковое представление объекта (отображается в админке)
    def __str__(self):
        return self.short_name


# -------------------------------------------------------------
#  Модель «Компания» — IT-компании, размещающие стажировки
# -------------------------------------------------------------
class Company(models.Model):
    # Список доступных значений для поля company_type.
    # Слева — что сохраняется в БД, справа — что видит пользователь
    COMPANY_TYPE_CHOICES = [
        ("commercial", "Коммерческая компания"),
        ("university", "Компания при вузе / НИИ"),
        ("startup", "Стартап"),
        ("government", "Государственная структура"),
    ]
    name = models.CharField("Название компании", max_length=255)
    # choices ограничивает значения списком COMPANY_TYPE_CHOICES.
    # В админке появится выпадающий список вместо текстового поля
    company_type = models.CharField(
        "Тип компании", max_length=20, choices=COMPANY_TYPE_CHOICES, default="commercial"
    )
    # ForeignKey — связь «многие к одному» (много компаний → один вуз).
    # on_delete=SET_NULL: если вуз удалят, у компании поле станет NULL,
    # сама компания не удалится
    university = models.ForeignKey(
        University,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Аффилированный вуз",
        related_name="companies",       # обратное обращение: university.companies.all()
    )
    description = models.TextField("Описание компании", blank=True)
    website = models.URLField("Сайт компании", blank=True)
    logo = models.ImageField("Логотип", upload_to="companies/", blank=True, null=True)
    contact_email = models.EmailField("Email для связи", blank=True)
    address = models.CharField("Адрес", max_length=255, blank=True)
    # Владелец аккаунта компании — пользователь, который её зарегистрировал.
    # Он может публиковать стажировки и отвечать на заявки от своего имени
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец аккаунта",
        related_name="companies",
    )
    # BooleanField — true/false; default=False означает, что новые компании
    # появляются неподтверждёнными, пока модератор их не проверит
    is_verified = models.BooleanField("Проверена", default=False)
    # auto_now_add=True — Django сам ставит текущую дату при создании записи
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
        ordering = ["name"]                   # сортировка по названию А–Я

    def __str__(self):
        return self.name


# -------------------------------------------------------------
#  Модель «Стажировка» — вакансии для студентов
# -------------------------------------------------------------
class Internship(models.Model):
    # Формат работы: офис / удалёнка / гибрид
    FORMAT_CHOICES = [
        ("office", "Офис"),
        ("remote", "Удалённо"),
        ("hybrid", "Гибрид"),
    ]
    # Направление работы — фильтр в каталоге
    FIELD_CHOICES = [
        ("backend", "Backend-разработка"),
        ("frontend", "Frontend-разработка"),
        ("fullstack", "Fullstack-разработка"),
        ("mobile", "Мобильная разработка"),
        ("devops", "DevOps / Инфраструктура"),
        ("data", "Data Science / ML / AI"),
        ("qa", "Тестирование (QA)"),
        ("design", "UI/UX Дизайн"),
        ("security", "Информационная безопасность"),
        ("pm", "Управление проектами (PM)"),
        ("other", "Другое"),
    ]

    # CASCADE — если компанию удалят, все её стажировки тоже удалятся
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, verbose_name="Компания", related_name="internships"
    )
    title = models.CharField("Название стажировки", max_length=255)
    field = models.CharField("Направление", max_length=20, choices=FIELD_CHOICES, default="other")
    description = models.TextField("Описание стажировки")
    image = models.ImageField("Изображение", upload_to="internships/", blank=True, null=True)
    requirements = models.TextField("Требования", blank=True)
    tasks = models.TextField("Задачи стажёра", blank=True)
    format = models.CharField("Формат работы", max_length=10, choices=FORMAT_CHOICES, default="office")
    duration = models.CharField("Продолжительность", max_length=100, blank=True,
                                help_text="Например: 2 месяца, лето 2025")
    stipend = models.CharField("Стипендия / Оплата", max_length=100, blank=True,
                               help_text="Например: 15 000 руб/мес или 'Не оплачивается'")
    # PositiveIntegerField — целое неотрицательное число (для мест отрицательных быть не может)
    spots = models.PositiveIntegerField("Количество мест", default=1)
    # ManyToManyField — связь «многие ко многим»: одна стажировка может быть
    # партнёрской для нескольких вузов, один вуз — для нескольких стажировок.
    # Django сам создаст промежуточную таблицу с двумя внешними ключами
    university_partnership = models.ManyToManyField(
        University,
        blank=True,
        verbose_name="Партнёрство с вузами",
        help_text="Вузы, студентам которых отдаётся предпочтение",
    )
    # Флаг активности — позволяет «скрыть» стажировку, не удаляя её из БД
    is_active = models.BooleanField("Активна", default=True)
    # DateField — только дата, без времени
    deadline = models.DateField("Дедлайн подачи заявок", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)   # дата создания
    updated_at = models.DateTimeField(auto_now=True)       # дата последнего изменения

    class Meta:
        verbose_name = "Стажировка"
        verbose_name_plural = "Стажировки"
        ordering = ["-created_at"]            # минус — сортировка по убыванию (новые первыми)

    def __str__(self):
        return f"{self.title} — {self.company.name}"

    # Доп. метод: возвращает число поданных заявок (используется в личном кабинете).
    # related_name="applications" из модели Application позволяет писать
    # self.applications вместо application_set
    def get_applications_count(self):
        return self.applications.count()


# -------------------------------------------------------------
#  Модель «Заявка» — отклик пользователя на стажировку
# -------------------------------------------------------------
class Application(models.Model):
    # Возможные статусы заявки. Меняются работодателем в его кабинете
    STATUS_CHOICES = [
        ("pending", "На рассмотрении"),
        ("reviewing", "Изучается"),
        ("interview", "Приглашён на интервью"),
        ("accepted", "Принят"),
        ("rejected", "Отказ"),
    ]

    # Связь с конкретной стажировкой
    internship = models.ForeignKey(
        Internship, on_delete=models.CASCADE, verbose_name="Стажировка", related_name="applications"
    )
    # Связь с пользователем, который подал заявку
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Соискатель",
        related_name="applications",
    )
    # Резюме: либо ссылка на hh.ru, либо файл (одно из двух — проверка в форме)
    hh_resume_url = models.URLField(
        "Ссылка на резюме hh.ru",
        blank=True,
        help_text="Вставьте ссылку на ваше резюме с hh.ru (например: https://hh.ru/resume/...)",
    )
    resume_file = models.FileField(
        "Резюме (файл)",
        upload_to="resumes/",
        blank=True,
        null=True,
        help_text="Загрузите резюме в формате PDF или DOCX",
    )
    cover_letter = models.TextField(
        "Сопроводительное письмо",
        blank=True,
        help_text="Расскажите, почему вы подходите для этой стажировки",
    )
    # Вуз и курс соискателя на момент подачи заявки
    university = models.ForeignKey(
        University,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Вуз соискателя",
    )
    course = models.CharField("Курс", max_length=20, blank=True, help_text="Например: 3 курс, магистратура 1 год")
    phone = models.CharField("Телефон", max_length=20, blank=True)
    # Статус заявки. По умолчанию — «На рассмотрении»
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="pending")
    # Поля для переписки работодатель → соискатель
    company_message = models.TextField(
        "Сообщение от компании",
        blank=True,
        help_text="Сообщение, которое отправляется соискателю",
    )
    company_message_at = models.DateTimeField(
        "Дата сообщения от компании", null=True, blank=True
    )
    # Флаг, сбрасывается в False при новом сообщении и ставится True,
    # когда соискатель открывает раздел «Мои заявки»
    company_message_read = models.BooleanField(
        "Прочитано соискателем", default=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]
        # unique_together = уникальная пара (стажировка, соискатель).
        # Защита от повторной подачи заявки на ту же стажировку
        unique_together = [["internship", "applicant"]]

    # Метод используется в шаблоне company_applications.html для построения dropdown статусов
    def get_status_choices(self):
        return self.STATUS_CHOICES

    def __str__(self):
        return f"{self.applicant.get_full_name() or self.applicant.username} → {self.internship.title}"
