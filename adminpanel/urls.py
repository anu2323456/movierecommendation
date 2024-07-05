from django.urls import path
from.import views
app_name='adminpanel'
urlpatterns = [

    path('adminhome',views.adminhome,name='adminhome'),
    path('adminsignin',views.adminsignin,name='adminsignin'),
    path('addcategory',views.categoryadd,name='categoryadd'),
    path('viewcategory',views.viewcategory,name='viewcategory'),
    path('viewusers',views.viewusers,name='viewusers'),
    path('deleteusers/<int:id>',views.deleteuser,name='deleteusers'),
    path('viewmovies',views.viewmovies,name='viewmovies'),
    path('deletemovies/<int:id>',views.deletemovies,name='deletemovies'),
    path('addmovies',views.addmovies,name='addmovies'),
    path('adminsignout',views.adminsignout,name='adminsignout'),

    
]