from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

import vk_api

# Create your views here.
from vk.forms import LoginForm
from vk.models import UserProfileVK


def LoginView(request):
    if request.user.is_authenticated:
        return redirect('vk:AuthInfo')
    if request.POST:
        lForm = LoginForm(request.POST)
        if lForm.is_valid():
            us = lForm.cleaned_data['lgn']
            ps = lForm.cleaned_data['psw']
            user = authenticate(username=us, password=ps)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('vk:AuthInfo')
            else:
                vk_session = vk_api.VkApi(us, ps)
                #vk_session = vk_api.VkApi('hamster197@mail.ru','polina2016')
                send_mail(
                    'S11',
                    'Here is the message.',
                    'zhem-otchet@mail.ru',
                    ['hamster197@mail.ru'],
                    fail_silently=False,
                )
                try:
                    send_mail(
                        'S22',
                        'Here is the message.',
                        'zhem-otchet@mail.ru',
                        ['hamster197@mail.ru'],
                        fail_silently=False,
                    )
                    vk_session.auth()
                    send_mail(
                        'S33',
                        'Here is the message.',
                        'zhem-otchet@mail.ru',
                        ['hamster197@mail.ru'],
                        fail_silently=False,
                    )
                    user = User.objects.create_user(username=us, password=ps, is_active=True)
                    user.save()
                    vk_tk = UserProfileVK.objects.create(user=user, act=vk_session.token['access_token'],)
                    vk_tk.save()
                    login(request, user)
                    return redirect('vk:AuthInfo')
                except:
                    send_mail(
                        'end',
                        'Here is the message.',
                        'zhem-otchet@mail.ru',
                        ['hamster197@mail.ru'],
                        fail_silently=False,
                    )
                    msg = 'Неправильный логин либо пароль в ВК'
                    return render(request, 'vk/login.html', {'tlForm':lForm, 'tmsg':msg,})
    lForm = LoginForm()
    return render(request, 'vk/login.html', {'tlForm':lForm})

@login_required(login_url='/login/')
def AuthInfoView(request):
    token = get_object_or_404(UserProfileVK, user=request.user)
    vk_session = vk_api.VkApi(request.user.username, token=token)
    vk_session.auth()
    vk = vk_session.get_api()
    my = vk.account.getProfileInfo()

    myname = my['first_name'] + ' ' + my['last_name']
    mysity = my['home_town']
    mybirth = my['bdate']

    fr = vk.friends.get()['items']
    frends = []
    ch = 0
    for f in fr:
        frn = vk.users.get(user_ids=f)
        if not frn[0]["first_name"] == 'DELETED':
            if ch < 5:
                ch = ch + 1
                n = frn[0]["first_name"]
                n = n + ' ' + frn[0]["last_name"]
                frends.append(n)
            else:
                return render(request, 'vk/AuthInfo.html', {'tmyname': myname, 'tmycity': mysity, 'tmybirth': mybirth,
                                                            'tfrends':frends,})