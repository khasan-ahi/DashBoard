from django.urls import path

from dashboard.views import HomePageView
from users.views import MyLoginView, logout_view, registration
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # path('', HomePageView.as_view(), name='home'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', registration, name='registration'),

]
