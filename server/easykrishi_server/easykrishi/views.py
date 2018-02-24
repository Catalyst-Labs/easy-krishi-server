from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

@login_required(login_url="/login/")
def loginFunction(request):
	if request.user.is_authenticated():
		# if request.user.is_superuser:
		# 	return HttpResponseRedirect('/admin/')
		# else:
		return HttpResponseRedirect('/user/api/v1/home/')
	else:
		return HttpResponseRedirect('/login/')

def index(request):
	"""
	"""	
	if request.method == 'POST':
		if 'username' in request.POST and 'password' in request.POST:
			form = AuthenticationForm(request, data=request.POST)
			if form.is_valid():
				user = authenticate(username=request.POST['username'], password=request.POST['password'])
				if user is not None:				
					login(request, user)				
					return HttpResponseRedirect('/user/api/v1/home/')
			else:
				return render(request, "app/index.html", {"form":form})

	if request.user.is_authenticated():
		return HttpResponseRedirect('/user/api/v1/home/')
	else:
		return render(request, "app/index.html", {})
