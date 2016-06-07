#!/usr/bin/python
# coding = utf-8
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from devop.views.permission import PermissionVerify, SelfPaginator
from opman.forms import EditUserForm


@login_required
@PermissionVerify()
def ListUser(request):
    mList = User.objects.all()
    lst = SelfPaginator(request, mList, 20)
    kwvars = {
        'lpage': lst,
        'request': request,
    }
    return render_to_response('UserManage/user.list.html', kwvars)


@login_required
@PermissionVerify()
def EditUser(request, ID):
    print(ID)
    user = User.objects.get(id=ID)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listuserurl'))
    else:
        form = EditUserForm(instance=user)

    kwvars = {
        'ID': ID,
        'form': form,
        'request': request,
    }

    return render_to_response('UserManage/user.edit.html', kwvars, RequestContext(request))


@login_required
@PermissionVerify()
def DeleteUser(request, ID):
    if ID == '1':
        return HttpResponse(u'超级管理员不允许删除!!!')
    else:
        User.objects.filter(id=ID).delete()

    return HttpResponseRedirect(reverse('listuserurl'))
