from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .utils import is_ajax, classify_face
import base64
from logs.models import Log
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from profiles.models import Profile
from .forms import userForm,profileForm
from django.contrib import messages

def login_view(request):
    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'main.html', {})

def find_user_view(request):
    if is_ajax(request):
        photo = request.POST.get('photo')
        _, str_img = photo.split(';base64')

        decoded_file = base64.b64decode(str_img)

        x = Log()
        x.photo.save('upload.png', ContentFile(decoded_file))
        x.save()

        res = classify_face(x.photo.path)
        if res:
            user_exists = User.objects.filter(username=res).exists()
            if user_exists:
                user = User.objects.get(username=res)
                profile = Profile.objects.get(user=user)
                x.profile = profile
                x.save()

                login(request, user)
                return JsonResponse({'message': 'profile matched successfully'})
        return JsonResponse({'message': 'profile did not match'})
    

def register_view(request):
    usr=User()
    if request.method=='POST':
        form=userForm(request.POST)
        form1=profileForm(request.POST,request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_present=User.objects.filter(username=username).exists()
            if user_present:
                return redirect('register')
            else:
                img=request.POST.get('img_url')
                _, img = img.split(';base64')
                decoded_file = base64.b64decode(img)

                user=form.save()
                user.username =  form.cleaned_data.get('username')
                user.set_password(password)
                user.save()
                # if form1.is_valid():
                x=Profile.objects.get(user=user) 
                file_name=x.user.username + '_' + str(x.user.id) +'.png'
                x.photo.save(file_name, ContentFile(decoded_file))
                x.save()
                    # profile=form1.save(commit=False)
                    # # profile.photo=request.FILES.get('photo')
                    # profile.photo('upload.png', ContentFile(decoded_file))
                    # profile.user=user
                    # profile.save()
                    # created=Profile.objects.create(photo=photo,user=user)
                    # messages.success(request,f"User Created Successfully.")
                return redirect('login')
    else:
        form = userForm()
        form1=profileForm()
    return render(request,'register.html', {'form':form,'form1':form1})