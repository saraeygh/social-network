from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import UserAccount
from posts.models import Post
from .forms import SignUpForm, SignInForm


class SignUp(View):
    def get(self, request):
        return render(request, 'signup.html', {'form': SignUpForm, 'host': request.get_host()})
    
    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            new_user = form.cleaned_data
            username = new_user['username']
            password = new_user['confirm_password']
            email = new_user['email']
            first_name = new_user['first_name']
            last_name = new_user['last_name']
            bio = new_user['bio']

            new_user = UserAccount.objects.create(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                bio=bio,
                )
            new_user.save()

        return redirect('useraccounts:userprofile', username)
    

class SignIn(View):
    def get(self, request):
        return render(request, 'signin.html', {'form': SignInForm, 'host': request.get_host()})
    
    def post(self, request):
        form = SignInForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data
            username = user['username']
            password = user['password']
            
            user = authenticate(
                request,
                username=username,
                password=password,
                )
            print(user)
            if user:
                login(request, user)
                return redirect(
                    'useraccounts:userprofile',
                    {'user': user}
                    )

        return redirect('useraccounts:userprofile', username)


class UserProfile(View):
    def get(self, request, username):
        user = UserAccount.objects.get(username=username)
        user_posts = Post.objects.filter(user=user.id)
        return render(
            request,
            'userprofile.html',
            {
                'user': user,
                'user_posts': user_posts,
                'host': request.get_host(),
                }
            )