from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post
from .filters import PostFilter


class BaseView(TemplateView):
    template_name = 'base.html'


class PostsList(ListView):
    model = Post
    ordering = 'post_datetime'
    template_name = 'posts.html'
    context_object_name = 'posts_list'
    paginate_by = 10


class PostsDetail(DetailView):
    model = Post
    template_name = 'singlepost.html'
    context_object_name = 'single_post'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create.html'


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')


class PostSearch(ListView):
    form_class = PostForm
    model = Post
    template_name = 'search.html'
    context_object_name = 'post_search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context
