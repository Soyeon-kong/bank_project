from django.http import  HttpRequest,HttpResponse
from django.shortcuts import render, redirect
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_view
from django.views.generic import CreateView, ListView,DetailView
from member.models import Member
# Create your views here.


def test(request):
    return render(request, 'member/test.html')

def login(request):
    return render(request, 'member/templates/registration/login.html')

class MemberCreate(CreateView):
    model = Member
    fields = ['id','pw','name','tel']
    template_name_suffix = '_create'
    success_url = reverse_lazy('login')

class MemberList(ListView):
    model = Member

def idConfirm(request):
    #id
    id = request.POST.get('id')
    # db안에
    result = Member.objects.get(pk=id)
    print(result)
    return HttpResponse(id)

def logincheck(request):
    id = request.POST.get('id')
    pw = request.POST.get('pw')
    print(id)
    print(pw)
    result = Member.objects.filter(pk=id,pw=pw)
    if result:
        request.session['id']=id
        return render(request,'deposit/test.html')
    else:
        return render(request,'registration/login.html')