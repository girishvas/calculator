"""calculator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from calculator.settings import MEDIA_ROOT,MEDIA_URL

from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from operations.views import *

# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router = DefaultRouter()
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Calculator API Documentation')

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('api/v1/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
	path('accounts/', include('rest_framework.urls', namespace='rest_framework')),

	path('api/v1/operations/', include('operations.urls')),
	path('api/docs/', schema_view),
]

urlpatterns += router.urls
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)