from django.contrib.auth.models import User
from .models import *
import datetime
import pdb
import math


def SimpleCalculation(user, operator, valOne, valTwo):
	if operator == 'add':
		value = valOne + valTwo
	elif operator == 'sub':
		value = valOne - valTwo
	elif operator == 'mul':
		value = valOne * valTwo
	elif operator == 'div':
		value = valOne / valTwo
	elif operator == 'pow':
		value = valOne ** valTwo
	elif operator == 'sqrt':
		value = math.sqrt(valOne)
	elif operator == 'fact':
		value = math.factorial(valOne)
	else:
		value = 'We cannot perform this operation'

	calcObj   				= Calculation()
	calcObj.user 			= User.objects.get(email=user)
	calcObj.firstValue 		= valOne
	calcObj.secondValue 	= valTwo
	calcObj.operation 		= operator
	calcObj.result 			= value
	calcObj.save()

	message = operator + " Operation performed successfully"
	result  = {"message": message, "value":value}
	return result


def ReportGeneration(value):
	now  = datetime.datetime.now()

	if value == 'today':
		calcObj				= Calculation.objects.filter(createdOn__day__lte =now.day,createdOn__day__gte=now.day,createdOn__month=now.month,createdOn__year=now.year).all()
	elif value == 'weekly':
		calcObj				= Calculation.objects.filter(createdOn__day__lte =now.day,createdOn__day__gte=now.day-7,createdOn__month=now.month,createdOn__year=now.year).all()
	elif value == 'monthly':
		calcObj				= Calculation.objects.filter(createdOn__month__lte =now.month,createdOn__month__gte=now.month-1,createdOn__year=now.year).all()
	elif value == 'yearly':
		calcObj				= Calculation.objects.filter(createdOn__year__lte =now.year,createdOn__year__gte=now.year).all()
	elif value == 'all':
		calcObj				= Calculation.objects.all()
	else:
		calcObj				= Calculation.objects.all()

	calcList 				= []
	for calc in calcObj:
		calcdict  			= {}
		data 				= calcdict
		data["ID"] 			= calc.id
		data["user"] 		= calc.user.email
		data["admin"] 		= True if calc.user.is_staff else False
		data["firstValue"] 	= calc.firstValue
		data["secondValue"] = calc.secondValue
		data["operation"]	= calc.operation
		data["result"] 		= calc.result
		data["createdOn"] 	= datetime.datetime.strftime(calc.createdOn,"%Y-%m-%d %H:%M")
		calcList.append(calcdict)

	result = {"count":calcObj.count(), "calcList":calcList}
	return result