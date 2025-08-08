from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password']
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})    


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session.get('user_registration_info')
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            now = timezone.now()
            if now - code_instance.created > timedelta(minutes=2):
                messages.error(request, 'The verification code has expired. Please try again.', 'danger')
                return redirect('accounts:verify_code')

            if int(cd['code']) == int(code_instance.code):
                User.objects.create_user(
                    phone_number = user_session['phone_number'],
                    email = user_session['email'],
                    full_name = user_session['full_name'],
                    password = user_session['password']
                )
                code_instance.delete()
                messages.success(request, 'Your account has been registered successfully.', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'Invalid verification code.', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.', 'success')
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_number=phone, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been logged in successfully.', 'success')
                return redirect('home:home')
            messages.error(request, 'Invalid phone number or password.', 'danger')
        return render(request, self.template_name, {'form': form})