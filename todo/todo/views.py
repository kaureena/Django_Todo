from django .shortcuts import render,redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import TODO
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        fnm=request.POST.get('fname')
        ename = request.POST.get('ename')
        pwd = request.POST.get('pwd')
        my_user = User.objects.create_user(fnm,ename,pwd)
        my_user.save()
        return redirect('/login')
    return  render (request,'signup.html')


def login_view(request):
    if request.method == 'POST':
        fnm=request.POST.get('fname')
        pwd=request.POST.get('pwd')
        user=authenticate(request,username=fnm, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/todo')
        else:
            return redirect('/login')
    return render(request,'login.html')

@login_required(login_url='/login')
def todo(request):
    if request.method=='POST':
        title = request.POST.get('title')
        obj=models.TODO(title=title, user=request.user)
        obj.save()
        res = models.TODO.objects.filter(user=request.user).order_by('-date')
        return redirect('/todo',{'res':res})
    res = models.TODO.objects.filter(user=request.user).order_by('-date')
    return render(request,'todo.html', {'res': res})

@login_required(login_url='/login')
def edit_todo(request,srno):
    if request.method=='POST':
        title = request.POST.get('title')
        obj=models.TODO.objects.get(srno=srno)
        obj.title=title
        obj.save()
        user=request.user  
        return redirect('/todo')
    
    obj=models.TODO.objects.get(srno=srno)
    return render(request,'todo.html',{'edit_obj': obj})

@login_required(login_url='/login')
def delete_todo(request,srno):
    obj = models.TODO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todo')

def signout(request):
    logout(request)
    return redirect('/login')