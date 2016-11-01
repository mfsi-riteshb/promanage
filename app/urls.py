from django.conf.urls import url,include
from django.contrib import admin
from . import views

app_name="app"
urlpatterns = [
    url(r'^login/$',views.app_login,name='login'),
    url(r'^register/$',views.app_register,name='register'),
    url(r'^forgot-password/$',views.app_forgot_password,name='forgot-password'),
    url(r'^logout/$',views.app_logout,name='logout'),
    url(r'^dashboard/$',views.app_dashboard,name='dashboard'),
    url(r'^verify/(?P<activation_key>[A-Za-z0-9]*)/$',views.app_verify,name='verify'),
    url(r'^change-password/$',views.app_change_password,name="change-password"),
    url(r'^edit-profile/$',views.app_edit_profile,name='edit-profile')
]
