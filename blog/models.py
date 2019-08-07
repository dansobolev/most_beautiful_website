from django.conf import settings
from django.db import models
from django.utils import timezone
from django.forms import ModelForm


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Email(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    message = models.CharField(max_length=300)


class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = [
            'username',
            'email',
            'message'
        ]


