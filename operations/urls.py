from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .views import *


urlpatterns = [
	# Authentication
	path('adduser/', AddUser.as_view(), name='adduser'),
	path('listuser/', ListUser.as_view(), name='listuser'),
	path('deleteuser/', DeleteUser.as_view(), name='deleteuser'),
	path('login/', Login.as_view(), name='login'),
	path('logout/', Logout.as_view(), name='logout'),
	# Operations
	path('simpleoperation/', SimpleOperation.as_view(), name='simpleoperation'),
	# path('simpleoperation/',login_required(SimpleOperation.as_view(), login_url=reverse_lazy('authentication:login')), name="simpleoperation"),
	path('report/', Report.as_view(), name='report'),
	path('download/', Download.as_view(), name='download'),
]