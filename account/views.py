from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.conf import settings
from account.forms import RegistrationForm, UserEditFrom
from account.models import UserBase
from account.token import account_activation_token
import threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_action_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your email'
    email_body = render_to_string('account/registration/account_activation_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email], )
    EmailThread(email).start()


@login_required
def dashboard(request):
    return render(request, 'account/user/dashboard.html')


def account_register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            send_action_email(user, request)

    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except():
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')

    return render(request, 'account/registration/activation_invalid.html')


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditFrom(isinstance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
        else:
            user_form = UserEditFrom(instance=request.user)

        return render(request, 'account/user/edit_details.html', {'user_form': user_form})
