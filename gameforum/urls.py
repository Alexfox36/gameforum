from board.views import BaseView, PostsList, PostsDetail, PostCreate, PostUpdate, PostDelete, PostSearch
from django.contrib import admin
from django.urls import path, include, re_path



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BaseView.as_view()),
    path('posts/', PostsList.as_view(), name='post_list'),
    path('posts/<int:pk>', PostsDetail.as_view(), name='post_detail'),
    path('posts/create/', PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('posts/search/', PostSearch.as_view(), name='post_search'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

    path('accounts/', include('allauth.urls')),




]
