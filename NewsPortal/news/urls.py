from django.urls import path
from .views import PostsList, PostDetail, PostsSearch, NewsCreate


urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', PostsSearch.as_view(), name='posts_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
]
