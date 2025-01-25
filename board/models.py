from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

CATEGORY_CHOICES = (("TN", "Танки"),
                    ("HL", "Хилы"),
                    ("DD", "ДД"),
                    ("TR", "Торговцы"),
                    ("GM", "Гилдмастры"),
                    ("QG", "Квестгиверы"),
                    ("KZ", "Кузнецы"),
                    ("KG", "Кожевники"),
                    ("ZV", "Зельевары"),
                    ("MZ", "Мастера заклинаний"),
                    )


class Subscription(models.Model):
    category_name = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    post_content = RichTextUploadingField()
    post_category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    post_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reply")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    comment_accept = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.comment_text[:30]}'


class OneTimeCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
