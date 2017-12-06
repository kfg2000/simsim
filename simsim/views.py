from django.shortcuts import render, redirect
from .forms import UserSignup, UserLogin
from django.contrib.auth import authenticate, login, logout

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


