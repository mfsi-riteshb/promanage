from django.conf.urls import url, include
from django.contrib import admin
from . import views
from .views import (
    LoginView, LogoutView, PasswordChangeView, DashBoardView, RegisterView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView,
    AccountVerifyView,EditProfileView
)
from django.contrib.auth import views as auth_views

app_name = "app"


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^profile/edit$', EditProfileView.as_view(), name='edit_profile'),
    url(r'^password_change/$', PasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change/done$', PasswordChangeDoneView.as_view(),
        name='password_change_done'),
    url(r'^password_reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^dashboard/$', DashBoardView.as_view(), name='dashboard'),
    url(r'^verify/(?P<activation_key>[A-Za-z0-9]*)/$',
        views.AccountVerifyView.as_view(), name='verify'),
]

