from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages


class UserRegisterView(View):
    form_class = UserRegistrationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.filter(phone_number=form.cleaned_data['phone']).first()
            if user:
                messages.error(request, 'User with this phone number already exists.', 'danger')
                return redirect('accounts:user_register')

            user = User.objects.filter(email=form.cleaned_data['email']).first()
            if user:
                messages.error(request, 'User with this email already exists.', 'danger')
                return redirect('accounts:user_register')

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
        return redirect('home:home')    


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
