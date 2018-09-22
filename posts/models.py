from django.db import models

# Create your models here.


class Post(models.Model):
    """ A model to store posts with the number of likes and dislikes. """

    user = models.ForeignKey(
        'auth.User',
        related_name='posts',
        on_delete=models.CASCADE,
        )

    title = models.CharField(
        max_length=255,
        default='',
        )

    text = models.TextField()

    likes = models.IntegerField(
        default=0,
        blank=True,
        )

    dislikes = models.IntegerField(
        default=0,
        blank=True,
        )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        )
