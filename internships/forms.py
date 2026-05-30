# =============================================================
#  forms.py — формы Django
# =============================================================
#  Форма — это объект, который:
#    1. Создаёт HTML-разметку полей <input> по описанию;
#    2. Принимает request.POST, проверяет каждое поле;
#    3. Возвращает либо «всё хорошо, вот cleaned_data»,
#       либо словарь с ошибками валидации.
#  ModelForm дополнительно умеет сохранять данные сразу в модель.
# =============================================================

from django import forms
# Готовые формы Django: регистрация и логин с проверкой пароля
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Application, Internship, Company


# -------------------------------------------------------------
#  Форма регистрации нового пользователя.
#  Наследуемся от UserCreationForm (уже умеет валидировать пароль)
#  и добавляем поля «Имя», «Фамилия», «Email».
# -------------------------------------------------------------
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=50)
    last_name = forms.CharField(label="Фамилия", max_length=50)
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        # Порядок отображения полей в HTML
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        # Конструктор вызывает родительский, затем мы добавляем CSS-классы
        # к каждому полю, чтобы они выглядели как Bootstrap-поля
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


# -------------------------------------------------------------
#  Форма входа. Берёт встроенную AuthenticationForm (она сама
#  проверит логин/пароль). Мы только добавляем CSS-класс.
# -------------------------------------------------------------
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


# -------------------------------------------------------------
#  Форма редактирования профиля
# -------------------------------------------------------------
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", max_length=50)
    last_name = forms.CharField(label="Фамилия", max_length=50)
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    # clean_<имя_поля> — кастомная проверка для одного поля.
    # Здесь проверяем, что email не занят другим пользователем
    def clean_email(self):
        email = self.cleaned_data["email"]
        # __iexact — точное совпадение без учёта регистра
        # exclude(pk=self.instance.pk) — исключаем самого пользователя
        # (иначе он не сможет сохранить свой же email)
        qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Этот email уже используется другим пользователем.")
        return email


# -------------------------------------------------------------
#  Форма подачи заявки на стажировку
# -------------------------------------------------------------
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        # Только эти поля выводим в форме (остальные заполнятся автоматически)
        fields = ["resume_file", "cover_letter", "university", "course", "phone"]
        # widgets — какие HTML-элементы и с какими атрибутами генерировать
        widgets = {
            "resume_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "cover_letter": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Расскажите о себе и своей мотивации...",
            }),
            "university": forms.Select(attrs={"class": "form-select"}),
            "course": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: 3 курс бакалавриата"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 (900) 000-00-00"}),
        }

    # Проверяем, что файл резюме приложен (теперь это обязательное поле)
    def clean_resume_file(self):
        resume_file = self.cleaned_data.get("resume_file")
        if not resume_file:
            raise forms.ValidationError("Необходимо прикрепить файл резюме (PDF или DOCX).")
        return resume_file


# -------------------------------------------------------------
#  Форма размещения стажировки (для работодателя)
# -------------------------------------------------------------
class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = [
            "title", "field", "description", "image", "requirements", "tasks",
            "format", "duration", "stipend", "spots", "university_partnership",
            "deadline",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "field": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "requirements": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "tasks": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "format": forms.Select(attrs={"class": "form-select"}),
            "duration": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: 3 месяца"}),
            "stipend": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: 20 000 руб/мес"}),
            # min=1 — нельзя поставить 0 или меньше мест
            "spots": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            # CheckboxSelectMultiple — список галочек для M2M-связи с вузами
            "university_partnership": forms.CheckboxSelectMultiple(),
            # type="date" — встроенный календарик в браузере
            "deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


# -------------------------------------------------------------
#  Форма регистрации компании
# -------------------------------------------------------------
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "company_type", "university", "description", "website", "logo", "contact_email", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "company_type": forms.Select(attrs={"class": "form-select"}),
            "university": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "contact_email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }


# -------------------------------------------------------------
#  Форма фильтрации каталога стажировок.
#  Обычная forms.Form (не ModelForm), поскольку данные никуда не
#  сохраняются — они нужны только для построения SQL-фильтра.
# -------------------------------------------------------------
class InternshipFilterForm(forms.Form):
    # Добавляем «пустое» значение в начало списков выбора
    FIELD_CHOICES = [("", "Все направления")] + list(Internship.FIELD_CHOICES)
    FORMAT_CHOICES = [("", "Любой формат")] + list(Internship.FORMAT_CHOICES)

    # required=False — поля необязательные, пользователь может ничего не выбирать
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Поиск по названию..."}),
    )
    field = forms.ChoiceField(choices=FIELD_CHOICES, required=False,
                              widget=forms.Select(attrs={"class": "form-select"}))
    format = forms.ChoiceField(choices=FORMAT_CHOICES, required=False,
                               widget=forms.Select(attrs={"class": "form-select"}))
