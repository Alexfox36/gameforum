
from django.contrib import admin
from django.urls import path, re_path, include

from board.views import BaseView, PostsList, PostsDetail, PostCreate, PostUpdate, PostDelete, PostSearch

from django.contrib import admin
from django.urls import path, include

from sign.views import main_view, login_view, otp_view, logout_view

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

    path('', main_view, name='main'),
    path('login/', login_view, name='login'),
    path('otp/', otp_view, name='otp'),
    path('logout/', logout_view, name='logout'),




]
