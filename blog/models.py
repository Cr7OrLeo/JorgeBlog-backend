from django.db import models

class Post(models.Model):
    CATEGORIES = [
        ('intro', 'Introduction'),
        ('update', 'site update'),
        ('other', 'other'),
    ]
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        default='other',
    )
    file = models.FileField(upload_to='/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
