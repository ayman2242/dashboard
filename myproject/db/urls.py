from django.urls import path, include
from .views import home,login_page,logout_page,director_autor, school,teacher_autor,add_user,success,teacher_detail,director_detail,school_detail
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

handler404 = 'yourapp.views.custom_page_not_found_view'

urlpatterns = [
    path('', home ,name="home"),
    path('login/',login_page, name= "login"),
    path('logout/',logout_page,name ="logout"),
    path('director/',director_autor,name = "director"),
    path('school/',school,name= "school"),
    path('teacher/',teacher_autor,name= "teacher_autor"),
    path('add_user/',add_user,name= "add_user"),
    path('success/school/<int:school_id>/', success, name='success_school'),
    path('success/director/<int:director_id>/',success, name='success_director'),
    path('success/teacher/<int:teacher_id>/', success, name='success_teacher'),
    path('teacher/<int:teacher_id>/',teacher_detail, name='teacher_detail'),
    path('school/<int:school_id>/',school_detail, name='school_detail'),
    path('director/<int:director_id>/',director_detail, name='director_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)