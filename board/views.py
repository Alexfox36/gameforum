from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post



class BaseView(TemplateView):
    template_name = 'base.html'


class PostsList(ListView):
    model = Post
    ordering = 'post_datetime'
    template_name = 'posts.html'
    context_object_name = 'posts_list'
    paginate_by = 10
    login_url = '/login/'
    redirect_field_name = ''


class PostsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'single_post'


# class PostCreate(CreateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'create.html'
#
#
# class PostUpdate(LoginRequiredMixin, UpdateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')


# class PostSearch(ListView):
#     form_class = PostForm
#     model = Post
#     template_name = 'search.html'
#     context_object_name = 'post_search'

