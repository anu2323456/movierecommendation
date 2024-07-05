from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

@login_required
def index(request):
    popularmovies=movielist.objects.filter(rating__gt=3)
    Englishmovies=movielist.objects.filter(Language='English')
    Malayalammovies=movielist.objects.filter(Language='Malayalam')
    category=Category.objects.all()
    return render(request,'home.html',{'popularmovies':popularmovies,'Englishmovies':Englishmovies,'Malayalammovies':Malayalammovies,'category':category})


def register(request):
    if request.method=='POST':
      username=request.POST.get('username')
      firstname=request.POST.get('Firstname')
      lastname=request.POST.get('Lastname')
      password=request.POST.get('password')
      email=request.POST.get('email')
      hashed_password = make_password(password)
      movieuser.objects.create(username=username,firstname=firstname,email=email,lastname=lastname,password=hashed_password)
      messages.success(request,'Welcome, You are sucessfully registered, now signin')
      return redirect('movies:signin')


    return render(request,'register.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        print(user)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('/home')  
        
        messages.error(request, 'Invalid username or password')

    return render(request, 'signin.html')

@login_required
def userprofile(request):
    try:
        user = request.user
        print('current logined user',user)
        m = get_object_or_404(movieuser, username=user.username)

        context = {
            'username': user.username,
            'firstname': m.firstname,
            'lastname': m.lastname,
            'email': m.email,
            'description':m.description,
            'profilepic': m.profilepic.url if m.profilepic else None,
        }

        return render(request, 'userprofile.html', context)

    except movieuser.DoesNotExist:
        # Handle the case where no movieuser object matches the username
        return render(request, 'userprofile.html', {'error_message': 'User profile not found.'})
    
@login_required
def useredit(request):
    user = request.user
    muser = movieuser.objects.filter(username=user).first()

    if request.method == 'POST':
        muser.firstname = request.POST.get('firstname', '')
        muser.lastname = request.POST.get('lastname', '')
        muser.email = request.POST.get('email', '')  # Ensure email field is properly named in the template
        muser.description = request.POST.get('description', '')
        
        if 'image' in request.FILES:
            muser.profilepic = request.FILES['image']
        
        muser.save()
        
        return redirect('/userprofile')  # Redirect to user profile page after saving
    
   
    return render(request,'useredit.html')


@login_required
def addmovie(request):
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
        selected_category=request.POST.get('category')
        print('selected_category',selected_category)
        trailerlink=request.POST.get('trailerlink')
        rating=request.POST.get('rating')
        review=request.POST.get('reviews')
        language=request.POST.get('Language')
        catid=Category.objects.get(id=selected_category)
        print('catid',catid)
        catname=catid.category_name

        movielist.objects.create(title=title,description=description,addeduser=m,poster=poster,Language=language,release_date=release_date,actors=actor,category=catid,trailerlink=trailerlink,rating=rating,reviews=review)
        return redirect('/home')

    return render(request,'addmovie.html',{'category':category})

@login_required
def moviedetail(request,id):
    movie=movielist.objects.get(id=id)
    return render(request,'moviedetail.html',{'moviedetail':movie})

@login_required
def categoryhome(request):
    category_param = request.GET.get('categories', '')
    category=Category.objects.all()
    
    if category_param:
        category_id, category_name = category_param.split(',')
        catmovies = movielist.objects.filter(category=category_id)
        catname = Category.objects.get(id=category_id)
    else:
        catmovies = movielist.objects.all()
        catname = None

    return render(request, 'categoryhome.html', {'catmovies': catmovies, 'catname': catname,'category':category})

@login_required
def movieedit(request, id):
    user = request.user
    categories = Category.objects.all()
    movie_user = movieuser.objects.get(username=user)
    movie = movielist.objects.get(id=id)

    if movie.addeduser == movie_user:
        if request.method == 'POST':
            movie.title = request.POST.get('title')
            movie.Language = request.POST.get('language')
            movie.description = request.POST.get('description')
            movie.release_date = request.POST.get('release_date')
            movie.actors = request.POST.get('actors')
            movie.poster = request.FILES.get('image')
            movie.category = Category.objects.get(id=request.POST.get('category'))
            movie.trailerlink = request.POST.get('trailerlink')
            movie.rating = request.POST.get('rating')
            movie.reviews = request.POST.get('reviews')
            movie.language = request.POST.get('language')
            movie.save()
            return redirect('/home')
        return render(request, 'movieedit.html', {'movie': movie, 'category': categories})
        
    else:
        messages.success(request,'You cant edit')
        return redirect('movies:moviedetail', id=id)
    
@login_required
def moviedelete(request,id):
    user=request.user
    movie_user = movieuser.objects.get(username=user)
    movie = movielist.objects.get(id=id)
    print(movie)

    if movie.addeduser == movie_user:
        movie.delete()
        return redirect('/home')
    else:
        message=messages.success(request,'You cant delete')
        return redirect('movies:moviedetail', id=id)
    
@login_required
def signout(request):
    user=request.user
    logout(request)
    return redirect('movies:signin')
        

@login_required
def aboutus(request):
    return render(request,'about.html')


@login_required   
def contact(request):
    return render(request,'contact.html')


@login_required
def search_movies(request):
    if request.method == 'GET':
        search_query = request.GET.get('query', '') 
        if search_query:
            movies = movielist.objects.filter(title__icontains=search_query)
            if movies.exists():
                context = {
                    'movies': movies,
                    'query': search_query,
                }
                messages.success(request, 'Results found for "{}"'.format(search_query))
            else:
                context = {
                    'query': search_query,
                }
                messages.info(request, 'No results found for "{}"'.format(search_query))
        else:
            context = {}
            messages.error(request, 'Please provide a search query')
        
        return render(request, 'searchresults.html', context)
    else:
        return redirect('/home')  
