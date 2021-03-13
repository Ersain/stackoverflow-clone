from django.db import models

from utils.utils import generate_uniq_code


class PostChoices(models.TextChoices):
    QUESTION = 'Question'
    ANSWER = 'Answer'


class Post(models.Model):
    code = models.CharField(
        db_index=True,
        max_length=32,
        default=generate_uniq_code,
        unique=True
    )
    post_type = models.CharField(
        choices=PostChoices.choices,
        default=PostChoices.QUESTION,
        max_length=255
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    accepted_answer = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    author = models.ForeignKey('users.Profile', on_delete=models.DO_NOTHING, related_name='posts')
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='children', null=True, blank=True)
    tags = models.ManyToManyField('main.Tag')


class Tag(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Comment(models.Model):
    question = models.ForeignKey('main.Post', on_delete=models.DO_NOTHING)
    body = models.TextField()
    rating = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('users.Profile', on_delete=models.DO_NOTHING)
