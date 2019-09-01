import json, pdb, string, random, os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import status

from rest_framework.decorators import permission_classes
from django.contrib.auth import login, logout, authenticate, get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse
from django.contrib.auth.decorators import login_required

import requests
from django.contrib.auth.models import User
from random import randint
from .models import *
from.applayer import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status , generics

from django.http import Http404, HttpResponse, HttpResponseRedirect
from math import ceil
import xlwt
now  = datetime.datetime.now()


class AddUser(generics.GenericAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = AddUserSerializer
	def post(self, request, *args, **kwargs):
		data = request.data

		try:
			firstName = data['first_name']
			# print(firstName)
		except:
			result = {"status":False,"message":"Please Enter the First Name"}
			return Response(result, status=status.HTTP_400_BAD_REQUEST)

		try:
			email = data['email']
			# print(email)
			if not User.objects.filter(email=email, is_active=True).count() == 0:
				result = {"status":False,"message":"Email is already register with us"}
				return Response(result, status=status.HTTP_400_BAD_REQUEST)
		except:
			result = {"status":False,"message":"Email id Missing"}
			return Response(result, status=status.HTTP_400_BAD_REQUEST)

		try:
			password = data['password']
			# print(password)
		except:
			result = {"status":False,"message":"password is Missing"}
			return Response(result, status=status.HTTP_400_BAD_REQUEST)

		try:
			is_admin = data['is_staff']
			print(is_admin)
			# print(is_admin)
			if is_admin == "true":
				admin = True
			else:
				admin = False
		except:
			admin = False
			pass

		userobj 			= User()
		userobj.first_name 	= firstName
		userobj.last_name 	= data['last_name']
		userobj.email 		= email
		userobj.username 	= email
		userobj.is_active 	= True
		userobj.is_staff 	= admin
		userobj.set_password(password)
		userobj.save()

		message = "Successfully " + userobj.first_name + " added to the system"
		result  = {"status":True, "message":message}
		return Response(result, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class ListUser(APIView):
	# permission_classes = (IsAuthenticated,)
	def get(self, request, *args, **kwargs):
		adminuser 				= User.objects.filter(is_staff=True).all()
		normaluser 				= User.objects.filter(is_staff=False).all()
		adminList 				= []
		normalList 				= []

		for user in adminuser:
			admindict 			= {}
			data 				= admindict
			data["userID"] 		= user.id
			data["first_name"] 	= user.first_name
			data["last_name"] 	= user.last_name
			data["email"] 		= user.email
			data["admin"]		= user.is_staff
			data["active"] 		= user.is_active
			adminList.append(admindict)
			
		for user in normaluser:
			normaldict 			= {}
			data 				= normaldict
			data["userID"] 		= user.id
			data["first_name"] 	= user.first_name
			data["last_name"] 	= user.last_name
			data["email"] 		= user.email
			data["admin"]		= user.is_staff
			data["active"] 		= user.is_active
			normalList.append(normaldict)


		result  = {"status":True, "adminList":adminList, "normalList":normalList,  "message":"User Listed completely"}
		return Response(result, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class DeleteUser(generics.GenericAPIView):
	# permission_classes = (IsAuthenticated,)
	serializer_class = DeleteSerializer
	def post(self, request, *args, **kwargs):
		data = request.data

		try:
			email = data['email']
			if User.objects.filter(email=email, is_active=True).count() == 0:
				result = {"status":False,"message":"Email is not register with us"}
				return Response(result, status=status.HTTP_400_BAD_REQUEST)
		except:
			result = {"status":False,"message":"Email id Missing"}
			return Response(result, status=status.HTTP_400_BAD_REQUEST)

		user 		= User.objects.filter(email=email)
		user.delete() 

		result  = {"status":True, "message":"User deleted Successfully"}
		return Response(result, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class Login(generics.GenericAPIView):
	serializer_class = LoginSerializer
	def post(self, request, *args, **kwargs):
		data = request.data
		try:
			username = data['username']
			profile = User.objects.filter(username=username)
			if profile.count() == 0:
				result = {"status":False,"message":"Username is not registered with us."}
				return Response(result, status=status.HTTP_400_BAD_REQUEST)
			if profile[0].is_active == False:
				result = {"status":False,"message":"User is suspented / deleted"}
				return Response(result, status=status.HTTP_400_BAD_REQUEST)
		except:
			result = {"status":False,"message":"Username is Missing"}
			return Response(result, status=status.HTTP_400_BAD_REQUEST)

		try:
			password = data['password']
		except:
			result = {"status":False,"message":"password is Missing"}
			return Response(result, status=status.HTTP_400_BAD_REQUEST)

		try:
			url = "http://127.0.0.1:8000/api/v1/token/"

			headers = {
				'Content-Type': "application/json",
				'cache-control': "no-cache",
			}

			payload  = {
				"username": username,
				"password": password
			}

			resp  	= requests.request("POST", url, data=json.dumps(payload), headers=headers)
			result  = {"status":True,"message":"Admin Logged in successfully", "values":json.loads(resp.text)}
			return Response(result, status=status.HTTP_200_OK)
		except:
			print("error in login")
			result = {"status":False,"message":"Login failed"}
			return Response(result, status=status.HTTP_201_CREATED)


@permission_classes((AllowAny, ))
class Logout(APIView):
	def post(self, request, *args, **kwargs):
		data = request.data
		print(data)
		try:
			token = data['token']
		except:
			result = {"status":False,"message":"Token Missing"}
			return Response(result, status=status.HTTP_200_OK)

		print(token)
		url = "http://127.0.0.1:8000/api/v1/token/refresh/"
		headers = {
			'Content-Type': "application/json",
			'cache-control': "no-cache",
		}
		payload  = {
			"refresh": token
		}
		resp 	= requests.request("POST", url, data=json.dumps(payload), headers=headers)
		values  = json.loads(resp.text)
		print(resp.text)
		logout(request)

		result = {"status":True,"message":"User Logged Out Successfully"}
		return Response(result, status=status.HTTP_200_OK)


class SimpleOperation(generics.GenericAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = CalculationSerializer
	def post(self, request, *args, **kwargs):
		data = request.data
		try:
			user = request.user.email
			admin = request.user.is_staff
		except:
			result = {"status":False,"message":"User data is not available"}
			return Response(result, status=status.HTTP_200_OK)			

		try:
			operator = data['operation']
			if admin == False and (operator == 'pow' or operator == 'sqrt' or operator == 'fact'):
				result = {"status":False,"message":"Access restricted to admin User"}
				return Response(result, status=status.HTTP_200_OK)
		except:
			result = {"status":False,"message":"Please Enter valid operator"}
			return Response(result, status=status.HTTP_400_BAD_REQUEST)

		try:
			valOne = int(data['firstValue'])
		except:
			result = {"status":False,"message":"Please Enter valid First Value"}
			return Response(result, status=status.HTTP_400_BAD_REQUEST)

		try:
			valTwo = int(data['secondValue'])
			if valTwo == 0 and operator == 'div':
				result = {"status":False,"message":"Division by Zero Error, Please change value"}
				return Response(result, status=status.HTTP_400_BAD_REQUEST)
		except:
			if operator == 'sqrt' or operator == "fact":
				valTwo = ''
				pass
			else:
				result = {"status":False,"message":"Please Enter valid Value for Second value"}
				return Response(result, status=status.HTTP_400_BAD_REQUEST)

		simplecalc 	= (SimpleCalculation(user, operator, valOne, valTwo))
		return Response(simplecalc, status=status.HTTP_200_OK)


class Report(generics.GenericAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = ReportSerializer
	def post(self, request, *args, **kwargs):
		data = request.data
		try:
			user = request.user.email
			admin = request.user.is_staff
		except:
			result = {"status":False,"message":"User data is not available"}
			return Response(result, status=status.HTTP_200_OK)

		try:
			report_of = data['report_of']
			if admin == False:
				result = {"status":False,"message":"Access restricted to admin User"}
				return Response(result, status=status.HTTP_200_OK)
		except:
			result = {"status":False,"message":"Please Enter valid parameter"}
			return Response(result, status=status.HTTP_400_BAD_REQUEST)

		report 	 = (ReportGeneration(report_of))

		return Response(report, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class Download(generics.GenericAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = ReportSerializer
	def post(self, request, *args, **kwargs):
		data = request.data
		try:
			user = request.user.email
			admin = request.user.is_staff
		except:
			result = {"status":False,"message":"User data is not available"}
			return Response(result, status=status.HTTP_200_OK)

		try:
			value = data['report_of']
			if admin == False:
				result = {"status":False,"message":"Access restricted to admin User"}
				return Response(result, status=status.HTTP_200_OK)
		except:
			result = {"status":False,"message":"Please Enter valid parameter"}
			return Response(result, status=status.HTTP_400_BAD_REQUEST)

		response = HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename="Report.xls"'
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('Report')

		row_num = 0

		font_style = xlwt.XFStyle()
		font_style.font.bold = True

		columns = ['User', 'First Value', 'Second Value', 'Operator', 'Result' ]

		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num], font_style)

		font_style = xlwt.XFStyle()

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
		
		rows = calcObj.values_list('user__email', 'firstValue', 'secondValue', 'operation', 'result')
		for row in rows:
			row_num += 1
			for col_num in range(len(row)):
				ws.write(row_num, col_num, row[col_num], font_style)

		wb.save(response)
		return response

		return Response(report, status=status.HTTP_200_OK)


from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class SwaggerSchemaView(APIView):
	permission_classes = [AllowAny]
	renderer_classes = [
		renderers.OpenAPIRenderer,
		renderers.SwaggerUIRenderer
	]

	def get(self, request):
		generator = SchemaGenerator()
		schema = generator.get_schema(request=request)

		return Response(schema)