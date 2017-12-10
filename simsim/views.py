from django.shortcuts import render, redirect
from .forms import UserSignup, UserLogin, CoffeeForm
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal
from .models import Bean, Roast, Syrup, Powder, Coffee
from django.http import JsonResponse
import json 

def usersignup(request):
	context = {}
	form = UserSignup()
	context['form'] = form

	if request.method=='POST':
		form = UserSignup(request.POST)
		if form.is_valid():
			user = form.save()
			username = user.username
			password = user.password

			user.set_password(password)
			user.save()

			auth_user = authenticate(username=username,password=password)
			login(request, user)
			return redirect('/')
		return redirect('simsim:signup')
	return render(request,'signup.html',context)

def userlogin(request):
	context = {}
	form = UserLogin()
	context['form'] = form

	if request.method=='POST':
		form = UserLogin(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = authenticate(username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('/')
			return redirect("simsim:login")
		return redirect("simsim:login")
	return render(request,'login.html',context)

def userlogout(request):
	logout(request)
	return redirect('/')


def coffee_price(coffee):
	total = coffee.bean.price + coffee.roast.price + (coffee.espresso_shot*Decimal(0.250))

	if coffee.syrups.all().count()>0:
		for s in coffee.syrups.all():
			total += s.price

	if coffee.powders.all().count()>0:
		for p in coffee.powders.all():
			total += p.price

	if coffee.steamed_milk:
		total += Decimal(0.100)

	return total

def create_coffee(request):
	context = {}
	if not request.user.is_authenticated:
		return redirect("simsim:login")
	form = CoffeeForm()

	if request.method=="POST":
		form = CoffeeForm(request.POST)
		if form.is_valid():
			coffee = form.save(commit=False)
			coffee.user = request.user
			coffee.save()
			form.save_m2m()
			coffee.price = coffee_price(coffee)
			coffee.save()
			return redirect('/')

	context["form"]= form
	return render(request, 'create_coffee.html', context)


def price(request):
	total = Decimal(0)

	bean_id = request.GET.get('bean')
	if bean_id:
		total += Bean.objects.get(id=bean_id).price

	roast_id = request.GET.get('roast')
	if roast_id:
		total += Roast.objects.get(id=roast_id).price

	shot_value = request.GET.get('shot')
	if shot_value:
		total += (int(shot_value)*Decimal(0.250))

	syrups = json.loads(request.GET.get('syrups'))
	if len(syrups)>0:
		for s in syrups:
			total += Syrup.objects.get(id=s).price

	powders = json.loads(request.GET.get('powders'))
	if len(powders)>0:
		for p in powders:
			total += Powder.objects.get(id=p).price

	milk = request.GET.get('milk')
	if milk == 'true':
		total += Decimal(0.100)


	return JsonResponse(round(total,3), safe=False)


