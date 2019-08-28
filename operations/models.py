from django.db import models
from django.contrib.auth.models import User
import datetime


'''
	add = addition
	sub = subtract
	mul = multiplication
	div = Division

	pow = power
	fact= factorial
	sqrt= square root
'''

class Calculation(models.Model):
	user 		= models.ForeignKey(User, on_delete=models.CASCADE)
	firstValue  = models.DecimalField(max_digits=50, decimal_places=3)
	secondValue = models.DecimalField(max_digits=50, decimal_places=3, null=True, blank=True)
	operation 	= models.CharField(max_length=40)
	result 		= models.DecimalField(max_digits=50, decimal_places=3)
	
	createdOn 	= models.DateTimeField(auto_now_add=True)
	updatedOn 	= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.operation