from django.urls import path
from . import views

urlpatterns = [
    path('generate_questions/', views.generate_questions, name='generate_questions'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.homePage, name='home'),
    path('savedquestion/', views.savedQuestionsPage, name='savedquestion'),
]
