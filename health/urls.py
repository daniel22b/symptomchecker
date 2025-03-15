from django.urls import path
from .views import register, user_login, user_logout, symptom_selection,recommend_disease, home, complete_profile, welcome

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("select-symptoms/", symptom_selection, name="select_symptoms"),
    path('recommendation', recommend_disease, name="recommend_disease" ),
    path("", home, name="home"),
    path("complete-profile/", complete_profile, name="complete_profile"),
    path("welcome/", welcome, name="welcome"),
]
