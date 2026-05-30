# =============================================================
#  views.py — представления (контроллеры) приложения
# =============================================================
#  Представление — это функция, которая получает HTTP-запрос
#  (request) и возвращает HTTP-ответ. Django сам сопоставляет
#  URL-адрес из urls.py с нужной функцией.
#  Жизненный цикл запроса:
#    Браузер → urls.py → views.py → models.py (БД) → templates → HTML
# =============================================================

from django.shortcuts import render, get_object_or_404, redirect  # вспомогательные функции
from django.contrib.auth import login, logout, authenticate        # система аутентификации
from django.contrib.auth.decorators import login_required          # декоратор: только для авторизованных
from django.contrib import messages                                # всплывающие уведомления (success/warning/error)
from django.db.models import Q, Count                              # Q — сложные условия в фильтрах; Count — для аннотирования
from django.core.paginator import Paginator                        # постраничное разбиение
from .models import Internship, Company, University, Application   # наши модели
from .forms import (                                                # формы Django
    ApplicationForm, InternshipForm, CompanyForm,
    RegisterForm, LoginForm, InternshipFilterForm, ProfileForm,
)


# -------------------------------------------------------------
#  Главная страница: hero-блок, статистика, последние стажировки
# -------------------------------------------------------------
def index(request):
    # filter(is_active=True) — берём только активные стажировки
    # select_related("company") — за один SQL-запрос подгружаем данные компании,
    # чтобы избежать проблемы N+1 (когда для каждой стажировки идёт отдельный запрос)
    # [:8] — срез первых 8 записей
    internships = Internship.objects.filter(is_active=True).select_related("company")[:8]
    # order_by("?") — случайный порядок (для разнообразия на главной)
    companies = Company.objects.filter(is_verified=True).order_by("?")[:8]
    universities = University.objects.all()
    # Словарь со счётчиками для блока статистики
    stats = {
        "internships": Internship.objects.filter(is_active=True).count(),
        "companies": Company.objects.filter(is_verified=True).count(),
        "universities": universities.count(),
    }
    # render — отрисовывает шаблон, передавая в него контекст (словарь)
    return render(request, "internships/index.html", {
        "internships": internships,
        "companies": companies,
        "universities": universities,
        "stats": stats,
    })


# -------------------------------------------------------------
#  Каталог стажировок: поиск, фильтрация, постраничный вывод
# -------------------------------------------------------------
def internship_list(request):
    # qs — queryset, отложенный (ленивый) набор записей из БД.
    # Django пока ничего не запрашивает — только готовит SQL
    qs = Internship.objects.filter(is_active=True).select_related("company")
    # Форма читает GET-параметры из URL (?q=...&field=...)
    form = InternshipFilterForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data.get("q")          # поисковое слово
        field = form.cleaned_data.get("field")  # направление
        fmt = form.cleaned_data.get("format")   # формат работы
        if q:
            # Q | Q — логическое ИЛИ, поиск по нескольким полям
            # icontains — поиск без учёта регистра (LIKE %...% в SQL)
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(company__name__icontains=q) |
                Q(description__icontains=q))
        if field:
            qs = qs.filter(field=field)
        if fmt:
            qs = qs.filter(format=fmt)
    # Paginator делит queryset на страницы по 6 элементов
    paginator = Paginator(qs, 6)
    page_number = request.GET.get("page")           # ?page=2 — текущая страница
    page_obj = paginator.get_page(page_number)      # объект страницы для шаблона
    return render(request, "internships/list.html", {"page_obj": page_obj, "form": form})


# -------------------------------------------------------------
#  Карточка стажировки (страница одного объекта)
# -------------------------------------------------------------
def internship_detail(request, pk):
    # get_object_or_404 — если запись с таким pk не найдена, вернётся 404 страница
    internship = get_object_or_404(Internship, pk=pk, is_active=True)
    already_applied = False
    if request.user.is_authenticated:
        # exists() — самый быстрый способ узнать, есть ли запись (SELECT 1 LIMIT 1)
        already_applied = Application.objects.filter(internship=internship, applicant=request.user).exists()
    return render(request, "internships/detail.html", {
        "internship": internship,
        "already_applied": already_applied,
    })


# -------------------------------------------------------------
#  Подача заявки на стажировку. @login_required — гость попадёт на /login/
# -------------------------------------------------------------
@login_required
def apply(request, pk):
    internship = get_object_or_404(Internship, pk=pk, is_active=True)
    # Защита от повторной подачи (уникальность также гарантирована в БД через unique_together)
    if Application.objects.filter(internship=internship, applicant=request.user).exists():
        messages.warning(request, "Вы уже подали заявку на эту стажировку.")
        return redirect("internship_detail", pk=pk)

    # Метод POST — пользователь отправил форму
    if request.method == "POST":
        # request.FILES нужен для загрузки файла резюме
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=False — создать объект без сохранения в БД,
            # чтобы вручную дописать недостающие поля
            application = form.save(commit=False)
            application.internship = internship
            application.applicant = request.user
            application.save()                  # теперь сохраняем
            messages.success(request, "Заявка успешно подана! Компания свяжется с вами.")
            return redirect("internship_detail", pk=pk)
    else:
        # Метод GET — показываем пустую форму
        form = ApplicationForm()

    return render(request, "internships/apply.html", {"form": form, "internship": internship})


# -------------------------------------------------------------
#  Каталог компаний с подсчётом активных стажировок
# -------------------------------------------------------------
def company_list(request):
    # annotate — добавляет к каждой записи вычисленное поле
    # active_internships = число связанных стажировок с is_active=True
    companies = Company.objects.filter(is_verified=True).annotate(
        active_internships=Count("internships", filter=Q(internships__is_active=True))
    )
    return render(request, "internships/companies.html", {"companies": companies})


# -------------------------------------------------------------
#  Карточка компании с её стажировками
# -------------------------------------------------------------
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk, is_verified=True)
    # company.internships — благодаря related_name="internships" в модели Internship
    internships = company.internships.filter(is_active=True)
    return render(request, "internships/company_detail.html", {
        "company": company,
        "internships": internships,
    })


# -------------------------------------------------------------
#  Список вузов с количеством компаний-партнёров
# -------------------------------------------------------------
def university_list(request):
    universities = University.objects.annotate(
        companies_count=Count("companies", filter=Q(companies__is_verified=True))
    )
    return render(request, "internships/universities.html", {"universities": universities})


# -------------------------------------------------------------
#  Размещение стажировки (доступно только владельцу компании)
# -------------------------------------------------------------
@login_required
def post_internship(request):
    # Проверяем, есть ли у пользователя зарегистрированная компания
    user_companies = Company.objects.filter(owner=request.user)
    if not user_companies.exists():
        messages.info(request, "Сначала зарегистрируйте компанию.")
        return redirect("register_company")

    if request.method == "POST":
        form = InternshipForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.company = user_companies.first()   # привязываем к компании пользователя
            internship.save()
            # save_m2m() нужен, потому что мы делали commit=False —
            # связи «многие ко многим» (партнёрские вузы) надо сохранять отдельно
            form.save_m2m()
            messages.success(request, "Стажировка успешно размещена!")
            return redirect("internship_detail", pk=internship.pk)
    else:
        form = InternshipForm()

    return render(request, "internships/post_internship.html", {
        "form": form,
        "companies": user_companies,
    })


# -------------------------------------------------------------
#  Регистрация / редактирование компании
# -------------------------------------------------------------
@login_required
def register_company(request):
    # Если у пользователя уже есть компания — открываем её для редактирования,
    # иначе создаём новую
    existing = Company.objects.filter(owner=request.user).first()
    if request.method == "POST":
        # instance=existing — если есть, форма обновит запись; если нет — создаст новую
        form = CompanyForm(request.POST, request.FILES, instance=existing)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            messages.success(request, "Профиль компании сохранён. После проверки модератором он будет опубликован.")
            return redirect("company_detail", pk=company.pk)
    else:
        form = CompanyForm(instance=existing)

    return render(request, "internships/register_company.html", {"form": form, "existing": existing})


# -------------------------------------------------------------
#  «Мои заявки» (для соискателя)
# -------------------------------------------------------------
@login_required
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user).select_related("internship", "internship__company")
    # При открытии страницы помечаем все непрочитанные сообщения от компаний как прочитанные.
    # exclude(company_message="") — только те заявки, где сообщение реально есть
    Application.objects.filter(
        applicant=request.user, company_message_read=False
    ).exclude(company_message="").update(company_message_read=True)
    return render(request, "internships/my_applications.html", {"applications": applications})


# -------------------------------------------------------------
#  «Заявки в мою компанию» (для работодателя)
# -------------------------------------------------------------
@login_required
def company_applications(request):
    companies = Company.objects.filter(owner=request.user)
    # __in — IN в SQL: «компания состоит в списке компаний пользователя»
    applications = Application.objects.filter(
        internship__company__in=companies
    ).select_related("internship", "applicant", "university")
    return render(request, "internships/company_applications.html", {"applications": applications})


# -------------------------------------------------------------
#  Изменение статуса заявки работодателем
# -------------------------------------------------------------
@login_required
def update_application_status(request, pk):
    # Условие internship__company__owner=request.user защищает: владелец чужой
    # компании не сможет менять статус заявок не своей компании
    application = get_object_or_404(Application, pk=pk, internship__company__owner=request.user)
    if request.method == "POST":
        new_status = request.POST.get("status")
        # Проверяем, что новое значение — из списка допустимых
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, "Статус заявки обновлён.")
    return redirect("company_applications")


# -------------------------------------------------------------
#  Отправка сообщения соискателю
# -------------------------------------------------------------
@login_required
def send_application_message(request, pk):
    from django.utils import timezone  # текущее время с учётом часового пояса
    application = get_object_or_404(Application, pk=pk, internship__company__owner=request.user)
    if request.method == "POST":
        # strip() убирает пробелы в начале/конце; or "" защищает от None
        text = (request.POST.get("message") or "").strip()
        if text:
            application.company_message = text
            application.company_message_at = timezone.now()
            application.company_message_read = False     # сбрасываем флаг при новом сообщении
            application.save()
            messages.success(request, f"Сообщение отправлено: {application.applicant.get_full_name() or application.applicant.username}")
        else:
            messages.warning(request, "Сообщение не может быть пустым.")
    return redirect("company_applications")


# -------------------------------------------------------------
#  Регистрация нового пользователя
# -------------------------------------------------------------
def register_view(request):
    if request.user.is_authenticated:
        # Если уже залогинен — отправляем на главную
        return redirect("index")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()              # создаём пользователя; пароль сразу хешируется
            login(request, user)            # автоматический вход после регистрации
            messages.success(request, f"Добро пожаловать, {user.first_name}!")
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "internships/register.html", {"form": form})


# -------------------------------------------------------------
#  Вход в систему
# -------------------------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        # Встроенная AuthenticationForm сама проверит логин/пароль
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.first_name or user.username}!")
            # Если на /login/?next=/cabinet/ — после входа отправим в /cabinet/
            next_url = request.GET.get("next", "index")
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, "internships/login.html", {"form": form})


# -------------------------------------------------------------
#  Выход из системы
# -------------------------------------------------------------
def logout_view(request):
    logout(request)                                 # удаляет сессию
    return redirect("index")


# -------------------------------------------------------------
#  Личный кабинет: статистика по заявкам + блок компании (если есть)
# -------------------------------------------------------------
@login_required
def dashboard(request):
    user = request.user

    # list(...) принудительно выполняет запрос и сохраняет результат в Python-список,
    # чтобы не запрашивать БД повторно при подсчётах и срезах
    applications_all = list(
        Application.objects
        .filter(applicant=user)
        .select_related("internship", "internship__company")
        .order_by("-created_at")
    )
    # Собираем словарь {статус: количество}
    status_counts = {key: 0 for key, _ in Application.STATUS_CHOICES}
    for app in applications_all:
        status_counts[app.status] = status_counts.get(app.status, 0) + 1

    # Проверяем, владеет ли пользователь компанией
    company = Company.objects.filter(owner=user).first()
    company_internships = []
    incoming_apps_all = []
    incoming_status_counts = {key: 0 for key, _ in Application.STATUS_CHOICES}
    if company:
        # Только для владельца компании дополнительно собираем его стажировки
        # и поступившие заявки
        company_internships = list(
            company.internships
            .annotate(apps_count=Count("applications"))   # сколько заявок на каждую стажировку
            .order_by("-created_at")
        )
        incoming_apps_all = list(
            Application.objects
            .filter(internship__company=company)
            .select_related("internship", "applicant")
            .order_by("-created_at")
        )
        for app in incoming_apps_all:
            incoming_status_counts[app.status] = incoming_status_counts.get(app.status, 0) + 1

    # Контекст передаётся в шаблон dashboard.html
    context = {
        "profile_user": user,
        "applications": applications_all[:5],            # последние 5 заявок
        "applications_total": len(applications_all),
        "status_counts": status_counts,
        "company": company,
        "company_internships": company_internships,
        "company_internships_count": len(company_internships),
        "incoming_apps": incoming_apps_all[:5],
        "incoming_apps_total": len(incoming_apps_all),
        "incoming_status_counts": incoming_status_counts,
    }
    return render(request, "internships/dashboard.html", context)


# -------------------------------------------------------------
#  Редактирование профиля пользователя
# -------------------------------------------------------------
@login_required
def profile_edit(request):
    if request.method == "POST":
        # instance=request.user — форма редактирует текущего пользователя
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён.")
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "internships/profile_edit.html", {"form": form})
