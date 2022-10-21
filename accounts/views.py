from django.shortcuts import render, redirect
from .forms import MyUserChangeForm, MyUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

# 회원가입
def signup(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return render(request, 'articles/index.html')
    else:
        form = MyUserCreationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/signup.html', context)

# 로그인
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data= request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/login.html', context)

# 로그아웃
def logout(reqeust):
    auth_logout(reqeust)
    return redirect('articles:index')    

# 회원정보조회
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        'user': user
    }
    return render(request, 'accounts/detail.html', context)

# 회원정보수정
def update(request, pk):
    if request.method == 'POST':
        form = MyUserChangeForm(request.POST, instance= request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail', request.user.pk)
    else:
        form = MyUserChangeForm(instance=request.user)
    context = {
        'form' : form ,
    }
    return render(request, 'accounts/update.html', context)

# 회원탈퇴
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('articles.index')


