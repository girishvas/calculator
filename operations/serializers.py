from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class CalculationSerializer(serializers.ModelSerializer):
	firstValue = serializers.Field(source='First Value', help_text="First Value")
	secondValue = serializers.Field(source='Second Value', help_text="Second Value")
	operation = serializers.Field(source='Operation', help_text="Operation ( add, sub, mul, div, pow, sqrt, fact )")
	
	class Meta:
		model = Calculation
		# fields = '__all__'
		fields = ('firstValue', 'secondValue', 'operation')


class AddUserSerializer(serializers.ModelSerializer):
	first_name = serializers.Field(source='First Name', help_text="First Name")
	last_name = serializers.Field(source='Last Name', help_text="Last Name")
	email = serializers.Field(source='Email', help_text="Email")
	password = serializers.Field(source='Password', help_text="Password")
	is_staff = serializers.Field(source='Is Admin', help_text="Is Admin value (True / False)")
	
	class Meta:
		model = User
		# fields = '__all__'
		fields = ('first_name', 'last_name', 'email', 'password', 'is_staff')


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=200, help_text="User Name")
	password = serializers.CharField(max_length=200, help_text="Password")
	
	class Meta:
		model = User
		fields = ( 'username', 'password')


class DeleteSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=200, help_text="Email")
	
	class Meta:
		model = User
		fields = ( 'email')


class ReportSerializer(serializers.Serializer):
	report_of = serializers.CharField(max_length=200, help_text="Type ( today, weekly, monthly, yearly )")
	
	class Meta:
		model = Calculation
		fields = ( 'report_of')