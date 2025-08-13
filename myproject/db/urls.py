from django.urls import path, include
from .views import home,login_page,logout_page
urlpatterns = [
    path('', home ,name="home"),
    path('login/',login_page, name= "login"),
    path('logout/',logout_page,name ="logout"),
    # path("qr/", generate_qr, name="generate_qr"),

]