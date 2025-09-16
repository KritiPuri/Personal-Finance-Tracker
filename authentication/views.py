from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib import auth
from django.db import transaction


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if User.objects.filter(email=email).exists():
            return JsonResponse({'emailerror': 'sorry email in use, choose another one'}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'usernameerror': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'usernameerror': 'sorry username in use, choose another one'}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValues': request.POST
        }
        try:
            with transaction.atomic():
                if not User.objects.filter(username=username).exists():
                    if not User.objects.filter(email=email).exists():
                        if len(password) < 6:
                            messages.error(request, 'Password too short')
                            return render(request, 'authentication/register.html', context)
                        user = User.objects.create_user(
                            username=username, email=email)
                        user.set_password(password)
                        user.save()
                        messages.success(
                            request, 'Account created successfully. You can now log in.')
                        return redirect('login')
        except Exception as e:
            messages.error(request, "Error Occured : "+str(e))
        return render(request, 'authentication/register.html', context)


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, "Welcome, " +
                                 user.username + " you are now logged in")
                return redirect('expenses')
            messages.error(request, "Invalid credentials, try again")
            return render(request, "authentication/login.html")
        messages.error(request, "Please fill all fields")
        return render(request, "authentication/login.html")


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            auth.logout(request)
            messages.success(request, "You have been logged out")
            return redirect('login')
        else:
            return redirect('login')
