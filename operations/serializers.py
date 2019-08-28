from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class CalculationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Calculation
		# fields = '__all__'
		fields = ('firstValue', 'secondValue', 'operation')


class AddUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		# fields = '__all__'
		fields = ('first_name', 'last_name', 'email', 'password', 'is_staff')


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=200)
	password = serializers.CharField(max_length=200)
	
	class Meta:
		model = User
		fields = ( 'username', 'password')


class DeleteSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=200)
	
	class Meta:
		model = User
		fields = ( 'email')


class ReportSerializer(serializers.Serializer):
	report_of = serializers.CharField(max_length=200)
	
	class Meta:
		model = Calculation
		fields = ( 'report_of')