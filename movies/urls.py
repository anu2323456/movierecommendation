from django.urls import path
from.import views
app_name='movies'
urlpatterns = [

    path('home',views.index,name='home'),
    path('register',views.register,name='register'),
    path('',views.signin,name='signin'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('useredit',views.useredit,name='useredit'),
    path('addmovie',views.addmovie,name='addmovie'),
    path('moviedetail/<int:id>',views.moviedetail,name='moviedetail'),
    path('category',views.categoryhome,name='categoryhome'),
    path('movieedit/<int:id>',views.movieedit,name='movieedit'),
    path('moviedelete/<int:id>',views.moviedelete,name='moviedelete'),
    path('signout',views.signout,name='signout'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('contact',views.contact,name='contactus'),
    path('search',views.search_movies,name='search'),
    
]