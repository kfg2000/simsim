from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Bean(models.Model):
	name = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=5, decimal_places=3, null=True)

	def __str__(self):
		return self.name

class Roast(models.Model):
	name = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=5, decimal_places=3, null=True)

	def __str__(self):
		return self.name

class Syrup(models.Model):
	name = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=5, decimal_places=3, null=True)

	def __str__(self):
		return self.name

class Powder(models.Model):
	name = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=5, decimal_places=3, null=True)

	def __str__(self):
		return self.name 
		

class Coffee(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	name = models.CharField(max_length=120)
	espresso_shot = models.PositiveIntegerField(default=1)
	bean = models.ForeignKey(Bean, on_delete=models.PROTECT)
	roast = models.ForeignKey(Roast, on_delete=models.PROTECT)
	syrups = models.ManyToManyField(Syrup, blank=True)
	powders = models.ManyToManyField(Powder, blank=True)
	water = models.FloatField(default=0.1)
	steamed_milk = models.BooleanField()
	foam = models.FloatField(default=0.2)
	extra_instructions = models.TextField(null=True, blank=True)
	price = models.DecimalField(max_digits=6, decimal_places=3, null=True)

	def __str__(self):
		return self.name









