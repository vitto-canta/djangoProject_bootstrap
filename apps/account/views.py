from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import Permission
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from apps.account.forms import RegistrationForm, DataForm
from apps.account.models import Account
from apps.costumer.models import Costumer
from apps.vendor.models import Vendor


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            is_costumer = form.cleaned_data['is_costumer']
            is_vendor = form.cleaned_data['is_vendor']

            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            country = form.cleaned_data['country']
            phone_number = form.cleaned_data['phone_number']
            postcode = form.cleaned_data['postcode']
            address_line_1 = form.cleaned_data['address_line_1']
            address_line_2 = form.cleaned_data['address_line_2']
            town_city = form.cleaned_data['town_city']

            user = Account.objects.create_user(email=email, username=username, is_costumer=is_costumer,
                                               is_vendor=is_vendor, name=name, surname=surname, country=country,
                                               phone_number=phone_number, postcode=postcode,
                                               address_line_1=address_line_1,
                                               address_line_2=address_line_2, town_city=town_city, is_active=True)
            user.set_password(password)
            user.save()
            normal_user_perm = (
                "can search item",
                "can view an item",
                "can view review rate",
                "can receive notifications"
            )

            for normal_user_perm_name in normal_user_perm:
                permission = Permission.objects.get(name=normal_user_perm_name)
                user.user_permissions.add(permission)
            if is_costumer:
                costumer = Costumer.objects.create(name=user.username, created_by=user)
                costumer.save()
                user.add_perm_costumer()

            if is_vendor:
                vendor = Vendor.objects.create(name=user.username, created_by=user)
                vendor.save()
                user.add_perm_vendor()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if not is_vendor and not is_costumer:
                messages.error(request, 'Account created but upgrade to costumer or vendor is recommended')
            else:
                messages.success(request, 'Account created successfully')

            return redirect('frontpage')

    else:
        form = RegistrationForm()

    return render(request, 'account/register.html', {'form': form})


@login_required
def personal_data(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = Account.objects.get(username=request.user)
            user.email = form.cleaned_data.get('email')
            user.phone_number = form.cleaned_data.get('phone_number')
            user.name = form.cleaned_data.get('name')
            user.surname = form.cleaned_data.get('surname')
            user.country = form.cleaned_data.get('country')
            user.town_city = form.cleaned_data.get('town_city')
            user.postcode = form.cleaned_data.get('postcode')
            user.address_line_1 = form.cleaned_data.get('address_line_1')
            user.address_line_2 = form.cleaned_data.get('address_line_2')
            user.save()
            messages.success(request, 'Account has been changed successfully')
            return redirect('frontpage')
        else:
            print(form.errors)

    else:
        form = DataForm(initial=model_to_dict(request.user))
    return render(request, 'account/personal_data.html', {'form': form})


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully')
            return redirect('frontpage')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'account/change_password.html', {
        'form': form
    })


@login_required()
def upgrade_costumer(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            check_if_user_exists = Account.objects.filter(username=username).exists()
            if check_if_user_exists:
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    if not user.is_costumer:
                        # this user is valid, do what you want to do
                        user = Account.objects.get(username=username)
                        user.is_costumer = True
                        user.save()
                        user.add_perm_costumer()
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        costumer = Costumer.objects.create(name=user.username, created_by=user)
                        costumer.save()
                        messages.success(request, "You've become a costumer")
                    else:
                        messages.error(request, 'You are already a costumer')
                    return redirect('frontpage')

    else:
        form = AuthenticationForm()
    return render(request, 'account/upgrade_costumer.html', {'form': form})


@login_required()
def upgrade_vendor(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            check_if_user_exists = Account.objects.filter(username=username).exists()

            if check_if_user_exists:
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    if not user.is_vendor:
                        # this user is valid, do what you want to do
                        user = Account.objects.get(username=username)
                        user.is_vendor = True
                        user.save()
                        user.add_perm_vendor()
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        vendor = Vendor.objects.create(name=user.username, created_by=user)
                        vendor.save()
                        messages.success(request, "You've become a vendor")
                    else:
                        messages.error(request, 'You are already a vendor')
                    return redirect('frontpage')
    else:
        form = AuthenticationForm()
    return render(request, 'account/upgrade_vendor.html', {'form': form})


@login_required()
def notification(request):
    return render(request, 'account/notifications.html')


@login_required()
def mark_notifications_read(request):
    notifications = request.user.notifications
    notifications.mark_all_as_read()
    return HttpResponseRedirect(request.GET.get('next'))
