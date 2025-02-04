from datetime import datetime

import generics
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.views import APIView

from .forms import PostForm
from .models import Post
from .filters import PostFilter

from django.utils import timezone
from .utils import generate_otp, Send_email_with_zoho_server

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterUserSerializer
from django.contrib.auth import get_user_model


class BaseView(TemplateView):
    template_name = 'base.html'


class PostsList(ListView):
    model = Post
    ordering = 'post_datetime'
    template_name = 'posts.html'
    context_object_name = 'posts_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostsDetail(DetailView):
    model = Post
    template_name = 'post.html'
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


User = get_user_model()

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            otp = generate_otp()    #new
            user.otp = otp    #new
            Send_email_with_zoho_server(    #new
                to_email=user.email,
                message=f'Your OTP for account verification is: {otp}'    #new
                )
            user.save()

            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                },
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            if 'email' in str(e) and 'unique' in str(e):
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

user_create = UserCreateAPIView.as_view()

class ValidateOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        print(user.otp)
        if user.otp == otp:
            # check if token has expired
            time_difference = max(user.created_at, user.updated_at)
            mins_difference = (
                timezone.now() - time_difference
            ).total_seconds() / 60
            if mins_difference > 2:
                response = {
                    "response_status": "error",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "OTP token expired. Try again.",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            user.otp_verified = True  # Mark OTP as verified
            user.otp = None
            user.save()

            # Authenticate the user and create or get an authentication token
            # token, _ = Token.objects.get_or_create(user=user)

            return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)