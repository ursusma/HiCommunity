# coding=utf-8
from __future__ import unicode_literals

import json

from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse
from django.db.models import Q
from common.constants.common import RET_FORMAT
from users.utils.security import request_method, login_required
from users import models as users_models
from users.constants.common import *
from users.utils import validation
from users.exception import *
from common.utils.js import js_str2bool


@request_method('GET')
def register_page(request):
    return render(request, 'users/register.html')


@request_method('POST')
def register(request):
    ret = RET_FORMAT
    password = request.POST.get('password')
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip().lower()
    # validation
    if (not validation.validate_username(username)
            or not validation.validate_email(email)):
        raise InvalidUsernameOrEmailFormat
    elif not validation.validate_password(password):
        raise InvalidPasswordFormat

    # uniqueness check
    user_objects = users_models.Account.objects.filter(Q(username=username) |
                                                       Q(email=email))
    if user_objects.count() > 0:
        raise UsernameOrEmailAlreadyExist
    try:
        users_models.Account.objects.create(password=password,
                                            username=username,
                                            email=email)
    except Exception as e:
        print('create user failed: %s' % str(e))
        raise UserAccountCreateFailed
    else:
        ret['result'] = True
        ret['msg']['redirect_url'] = reverse('accounts:login_page')
    return HttpResponse(json.dumps(ret))


@request_method('GET')
def login_page(request):

    return render(request, 'users/login.html')


@request_method('POST')
def login(request):
    # handle login user
    user_id = request.session.get(SESSION_LOGIN_USER)
    if user_id:
        raise UserAlreadyLogin

    ret = RET_FORMAT
    username_or_email = request.POST.get('username_or_email')
    password = request.POST.get('password')
    checked = js_str2bool(request.POST.get('checked'))

    # params validation
    if (not validation.validate_email(username_or_email) and not
            validation.validate_username(username_or_email)):
        raise InvalidUsernameOrEmailFormat
    elif not validation.validate_password(password):
        raise InvalidPasswordFormat
    else:
        username_or_email = username_or_email.strip()
        account_objects = users_models.Account.objects.filter(
            Q(email=username_or_email) | Q(username=username_or_email))
        if account_objects.count() == 1:
            account_object = account_objects[0]
            if account_object.password == password:
                # login successfully
                if not checked:
                    request.session.set_expiry(0)
                request.session[SESSION_LOGIN_USER] = {
                    'id': account_object.id,
                    'name': account_object.username,
                    'email': account_object.email,
                    'role': account_object.role
                }
                ret['result'] = True
            else:
                raise InvalidPassword
        else:
            raise UsernameOrEmailNotExist
    return HttpResponse(json.dumps(ret))


@login_required
@request_method('DELETE')
def logout(request, *args, **kwargs):
    ret = RET_FORMAT
    try:
        del request.session[SESSION_LOGIN_USER]
    except Exception as e:
        print('logout failed: %s' % str(e))
        raise UserLogoutFailed
    ret['result'] = True
    return HttpResponse(json.dumps(ret))
