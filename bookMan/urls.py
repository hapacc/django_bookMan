from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.login),
    url(r'^index',views.index),
    url(r'^student',views.stu),
    url(r'^borrow$',views.borrow),
    url(r'^borrow-books',views.borrow_books),
    url(r'^back-books',views.back_books),
    url(r'^accounts/',include('django.contrib.auth.urls')),
    url(r'^logout',logout_then_login),
    url(r'register',views.register),
]