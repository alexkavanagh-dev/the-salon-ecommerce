from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('FAQ/', views.frequently_asked_questions, name='FAQ'),
    path('FAQ/add', views.add_FAQ, name='add_FAQ'),
    path('privacy/', views.privacy_policy, name='privacy'),
]
