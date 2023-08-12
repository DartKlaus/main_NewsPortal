from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


class Author(models.Model):
    ratingAuthor = models.IntegerField(default=0)
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        postRat = Post.objects.filter(author_id=self.pk).aggregate(postRating=Coalesce(Sum('rating'), 0))['postRating']
        commentRat = Comment.objects.filter(user_id=self.authorUser).aggregate(commentRating=Coalesce(Sum('rating'), 0))['commentRating']
        postcomRat = Comment.objects.filter(post__author__authorUser=self.authorUser).aggregate(postcommentRating=Coalesce(Sum('rating'), 0))['postcommentRating']

        self.ratingAuthor = postRat * 3 + commentRat + postcomRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    article = 'AR'
    news = 'NE'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    post_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    text = models.TextField()
    position = models.CharField(max_length=2, choices=POSITIONS, default=news)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        small_text = self.text[0:123]+'...'
        return small_text

    def __str__(self):
        return f'{self.name}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
