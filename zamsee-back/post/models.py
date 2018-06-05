from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='post/%Y/%m/%d', blank=True, null=True)
    title = models.CharField(max_length=100)
    post = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    CATEGORY_CHOICES = (
        ('R', 're-view'),
        ('E', 'enter-view'),
        ('O', 'over-view'),
    )

    category = models.CharField(max_length=1,
                                choices=CATEGORY_CHOICES,
                                default='R')

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title
