from dashboard.views import HomePageView, CategoryAddView, PaymentAddView
from django.urls import path

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('category_add/', CategoryAddView.as_view(), name='category_add'),
    path('payment_add/<int:pk>', PaymentAddView.as_view(), name='payment_add'),
]
