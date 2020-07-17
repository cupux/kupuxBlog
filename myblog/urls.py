from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as as_views
app_name = 'myblog'

urlpatterns = [
    path('login/',as_views.LoginView.as_view(template_name='myblog/login.html'), name = 'login'),
    path('logout/',as_views.LogoutView.as_view(), name = 'logout'),
    path('', views.postList.as_view(), name='post'),
    path('contact/', views.contact, name='contact'),
    path('<int:year>/<int:month>/<slug:post>/',
            views.post_detail,
            name='post_detail'),
    path('subscribe/', views.subscribe, name='sub'),
    path('search',views.search, name = 'search'),
    path('save/', views.comment, name='comment'),
    path('category/<slug:pk>/',views.mycategory, name='filt'),
    path('createpost/', views.create, name='create'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('createcategory/', views.createCategory, name='createcategory'),
    
]