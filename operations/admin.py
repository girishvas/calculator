from django.contrib import admin
from .models import *


class CalculationAdmin(admin.ModelAdmin):
	list_display = ('user', 'firstValue', 'secondValue', 'operation', 'result', 'createdOn')
	list_filter = ['operation', 'createdOn']
	search_fields = ['operation']

admin.site.register(Calculation, CalculationAdmin)