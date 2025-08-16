from django.urls import path, include
from .views import home,login_page,logout_page,director_autor, school,teacher_autor
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home ,name="home"),
    path('login/',login_page, name= "login"),
    path('logout/',logout_page,name ="logout"),
    path('director/',director_autor,name = "director"),
    path('school/',school,name= "school"),
    path('teacher/',teacher_autor,name= "teacher_autor"),

    # path("qr/", generate_qr, name="generate_qr"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)