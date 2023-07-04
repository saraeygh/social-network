from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import UserAccount
from posts.models import Post
from .forms import SignUpForm, SignInForm, EditProfileForm


class SignUp(View):
    def get(self, request):
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'signup.html', context)
    
    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            new_user = form.cleaned_data
            username = new_user['username']
            password = new_user['password1']

            new_user = authenticate(request=request, username=username, password=password)
            login(request, new_user)
            return redirect('useraccounts:userprofile', username)
        
        else:
            errors = form.errors
            form = SignUpForm()
            context = {
                'form': form,
                'errors': errors,
                }
            return render(request, 'signup.html', context)


class SignIn(View):
    def get(self, request):
        form = SignInForm
        context = {'form': form}
        return render(request, 'signin.html', context)
    
    def post(self, request):
        form = SignInForm(request.POST)

        if form.is_valid():

            user = form.cleaned_data
            username = user['username']
            password = user['password']
            
            user = authenticate(
                request=request,
                username=username,
                password=password,
                )
                        
            if user:
                login(request=request, user=user)
                return redirect('useraccounts:userprofile', username)
            
            errors = form.errors
            form = SignInForm()
            context = {
                'form': form,
                'errors': errors
                }
            return render(request, 'signin.html', context)
        
        else:
            errors = form.errors
            form = SignInForm()
            context = {
                'form': form,
                'errors': errors
                }
        return render(request, 'signin.html', context)


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
                }
            )
    

class EditUserProfile(View):
    def get(self, request, username):
        user = UserAccount.objects.get(username=username)
        form = EditProfileForm(
            initial={
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'bio': user.bio,
                'image': user.image,
            }
            )

        context = {'form': form, 'user': user, 'host': request.get_host()}

        return render(request, 'editprofile.html', context)

    def post(self, request, username):
        user = UserAccount.objects.get(username=username)
        changes = EditProfileForm(request.POST, request.FILES, instance=user)

        if changes.is_valid():
            changes.save()         
            return redirect('useraccounts:userprofile', user)


class DeleteAccount(View):
    def get(self, request, username):
        user = UserAccount.objects.get(username=username)
        user.soft_delete = True
        user.save()

        return redirect('core:landing')


class SignOut(View):
    def get(self, request):
        logout(request)
        return redirect('core:landing')
