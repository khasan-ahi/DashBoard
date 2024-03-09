from django.urls import path
from dashboard.views import (HomePageView, CategoryAddView,
                             PaymentAddView, IncomeAddView,
                             CheckAddView,
                             CheckDeleteView, CheckUpdateView,
                             CheckTransferView)


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('category_add/', CategoryAddView.as_view(), name='category_add'),
    path('payment_add/<int:pk>', PaymentAddView.as_view(), name='payment_add'),
    path('income_add/<int:pk>', IncomeAddView.as_view(), name='income_add'),
    path('check_add/', CheckAddView.as_view(), name='check_add'),
    path('check_delete/<int:pk>', CheckDeleteView.as_view(), name='check_delete'),
    path('check_update/<int:pk>', CheckUpdateView.as_view(), name='check_update'),
    path('check_transfer/<int:pk>', CheckTransferView.as_view(), name='check_transfer'),
]
