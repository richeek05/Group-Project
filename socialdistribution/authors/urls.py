from django.urls import include, path
from .models import Author
from . import views

urlpatterns = [
    path('/login/', views.user_login, name='user_login'),
    path('/signup/', views.signup, name='signup'),
    path('/github/', views.GithubActivity.as_view(), name='github'),
    
    path('', views.AuthorList.as_view(), name = 'list'),
    path('/<uuid:id>', views.AuthorDetail.as_view(), name = 'detail'),
    path('/<uuid:id>/followers', views.FollowersList.as_view()),
    path('/<uuid:id>/followers/<uuid:fid>', views.FollowersDetail.as_view()),
    path('/<uuid:id>/posts', include('posts.urls')),
    path('/<uuid:id>/inbox', include('inbox.urls')),
]