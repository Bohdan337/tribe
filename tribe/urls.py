from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# This code block is defining the URL patterns for a Django project. Each `path` function call
# specifies a URL pattern and the corresponding view or include statement.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('user.urls')),
    path('', include('subject.urls')),
    path('', include('schedule.urls')),
    path('', include('units_test.urls')),
    path('captcha/', include('captcha.urls')),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
