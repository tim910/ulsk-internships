from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('internships.urls')),
    # Раздача загруженных media-файлов (логотипы и фото компаний).
    # На Render нет отдельного nginx, поэтому отдаём их через Django —
    # и в разработке, и в продакшене (для учебного проекта это нормально).
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
