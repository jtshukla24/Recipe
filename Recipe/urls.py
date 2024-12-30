from django.contrib import admin
from django.urls import path
from app1.views import *
from report.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # path('',home, name ="home"),
    path('', login_page, name="login_page"),
    path('admin/', admin.site.urls),
    path('delete_recipe/<id>/', delete_recipe, name="delete_recipe"),
    path('update_recipe/<id>/', update_recipe, name="update_recipe"),
    path('recipe/', recipe, name="recipe"),
    path('register/', register, name="register"),
    path('logout/', logout_page, name="logout_page"),
    path('get_students/', get_students, name='get_students'),
    path('see_marks/<student_id>/', see_marks, name="see_marks")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
