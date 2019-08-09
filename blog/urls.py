from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('profile/', views.yourprofile, name='yourprofile'),
    path('contact/', views.contact_us, name='contact'),
    path('sent_successfully/', views.send_email_function, name='send_success'),
    path('test-user-page/', views.test_user_page, name='test_user_page'),
]