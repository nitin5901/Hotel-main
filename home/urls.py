from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [

    path("", views.index, name='index'),
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='contact'),
    path("book/table", views.booking, name='book'),
    path("ratings/", views.rating, name='rate'),
    path("admin123/", views.admin_page, name='admin-pg'),

    path("register/", views.register, name='register'),
    path("login/", views.login_request, name='login'),
    path("logout/", views.logout_request, name='logout'),

]

