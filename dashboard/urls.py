from dashboard.views import (HomePageView, CategoryAddView,
                             PaymentAddView, CheckAddView,
                             CheckDeleteView, CheckUpdateView,
                             CheckTransferView)
from django.urls import path

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('category_add/', CategoryAddView.as_view(), name='category_add'),
    path('payment_add/<int:pk>', PaymentAddView.as_view(), name='payment_add'),
    path('check_add/', CheckAddView.as_view(), name='check_add'),
    path('check_delete/<int:pk>', CheckDeleteView.as_view(), name='check_delete'),
    path('check_update/<int:pk>', CheckUpdateView.as_view(), name='check_update'),
    path('check_transfer/<int:pk>', CheckTransferView.as_view(), name='check_transfer'),
]
