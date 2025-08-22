from django.urls import path, include
from .views import home,login_page,logout_page,director_autor, school,teacher_autor,add_user,success,teacher_detail,director_detail,school_detail,school_list,delete_school,directors_list,delete_director,teacher_list,delete_teacher,director_views,edit_director,user_list,user_views,school_views,teacher_views,edit_school,edit_teacher,edit_user,delete_user
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



    # for director remove modified add and views 
    path('director/<int:director_id>/edit/', edit_director, name='edit_director'),
    path('teacher/<int:teacher_id>/edit/', edit_teacher, name='edit_teacher'),
    path('school/<int:school_id>/edit/', edit_school, name='edit_school'),
    path('user/<int:user_id>/edit/', edit_user, name='edit_user'),
    #views path
    path('director/detail/<int:director_id>/', director_views, name='director_views'),
    path('teacher/detail/<int:teacher_id>/', teacher_views, name='teacher_views'),
    path('school/detail/<int:school_id>/', school_views, name='school_views'),
    path('user/detail/<int:user_id>/', user_views, name='user_views'),

    #delete path
    path('schools/delete/<int:school_id>/', delete_school, name='delete_school'),
    path('directors/delete/<int:director_id>/', delete_director, name='delete_director'),
    path('teachers/delete/<int:teacher_id>/', delete_teacher, name='delete_teacher'),
    path('user/delete/<int:user_id>/', delete_user, name='delete_user'),


    #list path or table 
    path('schools/', school_list, name='school_list'),
    path('teachers/', teacher_list, name='teacher_list'),
    path('directors/', directors_list, name='directors_list'),
    path("users/", user_list, name="user_list"),





]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)