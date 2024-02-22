from django.urls import path, reverse_lazy

from users.views import MyLoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

]
