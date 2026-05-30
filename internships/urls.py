# =============================================================
#  urls.py — таблица маршрутов приложения
# =============================================================
#  Django проходит по списку urlpatterns сверху вниз, сравнивает
#  URL запроса с каждым шаблоном и вызывает соответствующую функцию
#  из views.py. Параметры из URL (например, <int:pk>) передаются
#  в функцию-обработчик как аргументы.
#
#  path(маршрут, функция-обработчик, name=имя)
#    name — символическое имя маршрута, используется в шаблонах
#    и redirect-ах: {% url 'internship_detail' pk=5 %}
# =============================================================

from django.urls import path
from . import views                # импорт всех представлений из соседнего файла

urlpatterns = [
    # Главная страница: /
    path("", views.index, name="index"),

    # Каталог стажировок и карточки
    path("internships/", views.internship_list, name="internship_list"),
    # <int:pk> — целое число pk (primary key) из URL передаётся в функцию
    path("internships/<int:pk>/", views.internship_detail, name="internship_detail"),
    path("internships/<int:pk>/apply/", views.apply, name="apply"),
    path("internships/post/", views.post_internship, name="post_internship"),

    # Компании
    path("companies/", views.company_list, name="company_list"),
    path("companies/<int:pk>/", views.company_detail, name="company_detail"),
    path("companies/register/", views.register_company, name="register_company"),

    # Вузы
    path("universities/", views.university_list, name="university_list"),

    # Личный кабинет соискателя: «Мои заявки»
    path("my/applications/", views.my_applications, name="my_applications"),

    # Личный кабинет работодателя: «Заявки в мою компанию» + действия
    path("my/company/applications/", views.company_applications, name="company_applications"),
    path("my/company/applications/<int:pk>/status/", views.update_application_status, name="update_application_status"),
    path("my/company/applications/<int:pk>/message/", views.send_application_message, name="send_application_message"),

    # Регистрация, вход, выход
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Личный кабинет (сводный) и редактирование профиля
    path("cabinet/", views.dashboard, name="dashboard"),
    path("cabinet/edit/", views.profile_edit, name="profile_edit"),
]
