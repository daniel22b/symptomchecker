from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from health.views import UserView, UserProfileView

router = routers.DefaultRouter()
router.register(r'profiles', UserProfileView)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("health.urls")),
    path("api/", include(router.urls))
]


#sudo systemctl stop django
