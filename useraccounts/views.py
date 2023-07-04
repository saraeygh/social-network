from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import UserAccount
from posts.models import Post
from .forms import SignUpForm, SignInForm, EditProfileForm


class SignUp(View):
    def get(self, request):
        context = {'form': SignUpForm, 'host': request.get_host()}
        return render(request, 'signup.html', context)
    
    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            new_user = form.cleaned_data
            UploadedFile.read()
            print(new_user['profile_image'])
            print(request.FILES['profile_image'])

            username = new_user['username']
            username = SignUpForm.check_username(form, username)
            password = new_user['password2']
            email = new_user['email']
            first_name = new_user['first_name']
            last_name = new_user['last_name']
            bio = new_user['bio']
            profile_image = request.FILES['profile_image']

            new_user = UserAccount.objects.create_user(username=username, password=password)
            new_user.email = email
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.bio = bio
            new_user.profile_image = profile_image
            new_user.save()


            return redirect('useraccounts:userprofile', username)
        else:
            print(form.errors)
            form = SignUpForm()
            context = {'form': form, 'host': request.get_host()}
            return render(request, 'signup.html', context)
        
    

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

        return render(
            request,
            'editprofile.html',
            {
                'form': form,
                'user': user,
                'host': request.get_host(),
                }
            )
    
    def post(self, request, username):
        user = UserAccount.objects.get(username=username)
        changes = EditProfileForm(request.POST)

        if changes.is_valid():
            changes = changes.cleaned_data
            print(changes)
            user.username = changes['username']
            new_username = changes['username']
            print(new_username, type(new_username))
            user.save()

            new_user_info = UserAccount.objects.get(username=new_username)
            return redirect('useraccounts:userprofile', {'user': new_user_info})
        

class DeleteAccount(View):
    def get(self, request, username):
        print(username, type(username))
        user = UserAccount.objects.get(username=username)
        user.soft_delete = True
        user.save()

        return redirect('core:landing')