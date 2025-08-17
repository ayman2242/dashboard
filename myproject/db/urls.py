from django.urls import path, include
from .views import home,login_page,logout_page,director_autor, school,teacher_autor,add_user,success
from django.conf import settings
from django.conf.urls.static import static

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
    

    # path("qr/", generate_qr, name="generate_qr"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)