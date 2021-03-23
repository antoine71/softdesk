from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.MyTokenObtainView.as_view(), name='token_obtain'),
    path('signup/', views.CreateUserView.as_view()),
]
