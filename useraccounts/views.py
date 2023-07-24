from typing import Any
from django import http
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from posts.models import Post
from .models import UserAccount, Relation
from .forms import SignUpForm, SignInForm, EditProfileForm


class SignUp(View):

    def get(self, request):
        form = SignUpForm()
        context = {'form': form}

        return render(request, 'signup.html', context)

    def post(self, request, **args):
        form = SignUpForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)

            if UserAccount.objects_all.filter(username=new_user.username).exists():
                errors = Exception("A user with that username already exists")
                form = SignUpForm()
                context = {
                    'form': form,
                    'errors': errors,
                    }
                return render(request, 'signup.html', context)

            new_user.save()
            login(request, new_user)

            return redirect('useraccounts:userprofile', new_user.username)

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
            
            errors = Exception('Incorrect username or password, try again.')
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

        context = {
            'user': user,
            'user_posts': user_posts
        }

        return render(request, 'userprofile.html', context)


class EditUserProfile(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.user = UserAccount.objects.get(username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.id is self.user.id:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, 'userprofile.html', {'user': request.user})

    def get(self, request, username):
        form = EditProfileForm(
            initial={
                'username': self.user.username,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'bio': self.user.bio,
                'image': self.user.image,
            }
            )

        context = {'form': form, 'user': self.user, 'host': request.get_host()}

        return render(request, 'editprofile.html', context)

    def post(self, request, username):
        changes = EditProfileForm(request.POST, request.FILES, instance=self.user)

        if changes.is_valid():
            changes.save()
            return redirect('useraccounts:userprofile', self.user)


class DeleteAccount(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.user = UserAccount.objects.get(username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.id is self.user.id:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, 'userprofile.html', {'user': request.user})

    def get(self, request, username):
        self.user.soft_delete = True
        self.user.save()

        return redirect('core:landing')


class SignOut(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('core:landing')


class Follow(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.from_user = request.user
        self.to_user = UserAccount.objects.get(username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, username):

        if self.from_user == self.to_user:
            return redirect('useraccounts:userprofile', self.to_user.username)

        is_following = Relation.objects.filter(from_user=self.from_user, to_user=self.to_user).exists()
        if is_following:
            return redirect('useraccounts:userprofile', self.to_user.username)
        
        Relation(from_user=self.from_user, to_user=self.to_user).save()
        return redirect('useraccounts:userprofile', self.to_user.username)


class Unfollow(LoginRequiredMixin, View):

    def setup(self, request, *args, **kwargs):
        self.from_user = request.user
        self.to_user = UserAccount.objects.get(username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, username):

        if self.from_user == self.to_user:
            return redirect('useraccounts:userprofile', self.to_user.username)

        is_following = Relation.objects.filter(from_user=self.from_user, to_user=self.to_user).exists()
        if is_following:
            Relation.objects.filter(from_user=self.from_user, to_user=self.to_user).delete()
            return redirect('useraccounts:userprofile', self.to_user.username)

        return redirect('useraccounts:userprofile', self.to_user.username)


class Search(View):

    def get(self, request):
        
        username = request.GET.get('username')
        
        exact_user = UserAccount.objects.filter(username=username)
        similar_users = UserAccount.objects.filter(username__icontains=username)

        context = {
            'username': username,
            'exact_user': exact_user,
            'similar_users': similar_users,
        }

        return render(request, 'search_user.html', context)
