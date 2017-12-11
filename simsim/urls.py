from . import views
from django.urls import path

app_name="simsim"

urlpatterns = [
	path('signup/',views.usersignup, name='signup'),
	path('login/',views.userlogin, name='login'),
	path('logout/', views.userlogout, name='logout'),
	path('create_coffee/', views.create_coffee, name='create'),
	path('price/', views.price, name="price"),
	path('app/', views.application, name="application"),
	path('',views.list,name='list'),
	path('detail/<int:coffee_id>',views.detail,name='detail'),
]