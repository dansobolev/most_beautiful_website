from django.urls import path
from . import views

urlpatterns = [
    path('payment/charge/', views.charge, name='charge'),
    path('payment/', views.HomePageView.as_view(), name='payment'),
]