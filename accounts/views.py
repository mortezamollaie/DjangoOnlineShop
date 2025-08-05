from django.shortcuts import render
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm
import random
from utils import send_otp_code
from .models import OtpCode
from django.contrib import messages


class UserRegisterView(View):
    form_class = UserRegistrationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(100000, 999999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
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


    def get(self, request):
        pass

    def post(self, request):
        pass

