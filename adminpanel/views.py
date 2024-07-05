from django.shortcuts import render

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from movies.models import *
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def adminhome(request):
    return render(request,'test.html')


def adminsignin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user and user.is_superuser:
            login(request, user)
            return redirect('/adminhome')  
        else:
           
            return render(request, 'adminsignin.html', {'error': 'Invalid credentials or access denied.'})
    
    return render(request, 'adminsignin.html')


@user_passes_test(is_admin)
def categoryadd(request):
    if request.method=='POST':
        name=request.POST.get('categoryname')
        Category.objects.create(category_name=name)
        return redirect('/viewcategory')

    return render(request,'addcategoryadmin.html')

@user_passes_test(is_admin)
def viewcategory(request):
    categories=Category.objects.all()
    return render(request,'viewcategoryadmin.html',{'category':categories})

@user_passes_test(is_admin)
def viewusers(request):
    userlist=movieuser.objects.all()
    return render(request,'useradmin.html',{'userlist':userlist})

@user_passes_test(is_admin)
def deleteuser(request,id):
    user=movieuser.objects.get(id=id)
    user.delete()
    return redirect('/viewusers')

@user_passes_test(is_admin)
def viewmovies(request):
    movielistt=movielist.objects.all()
    return render(request,'moviesadmin.html',{'movielistt':movielistt})

@user_passes_test(is_admin)
def deletemovies(request,id):
    movie=movielist.objects.get(id=id)
    movie.delete()
    return redirect('/viewmovies')

@user_passes_test(is_admin)
def addmovies(request):
    
    category=Category.objects.all()
    user=request.user
    m=movieuser.objects.get(username=user)
    usrid=m.id
    if request.method=='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        release_date=request.POST.get('release_date')
        actor=request.POST.get('actors')
        poster=request.FILES['image']
        print(poster)
        selected_category=request.POST.get('category')
        print('selected_category',selected_category)
        trailerlink=request.POST.get('trailerlink')
        rating=request.POST.get('rating')
        review=request.POST.get('reviews')
        catid=Category.objects.get(id=selected_category)
        print('catid',catid)
        catname=catid.category_name

        movielist.objects.create(title=title,addeduser=m,poster=poster,release_date=release_date,description=description,actors=actor,category=catid,trailerlink=trailerlink,rating=rating,reviews=review)
        return redirect('/viewmovies')

    return render(request,'addmovieadmin.html',{'category':category})




@user_passes_test(is_admin)
def adminsignout(request):
    user=request.user
    logout(request)
    return redirect('/adminsignin')
        







