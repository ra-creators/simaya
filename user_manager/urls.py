from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm

urlpatterns = [
    path('login/',views.login_page, name="login"),
    path('logout/',views.logout_page,name="logout"),
    path('signup/',views.signup_page,name="signup"),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name="userform/password_reset.html",form_class=PasswordResetForm),name="password_reset"),

    path('password_rese/done/',auth_views.PasswordResetDoneView.as_view(template_name="userform/password_reset_done.html"),name="password_reset_done"),
    
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="userform/password_reset_confirm.html" ,form_class=SetPasswordForm),name="password_reset_confirm"),
    
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="userform/password_reset_complete.html"),name="password_reset_complete"),  
]