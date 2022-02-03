from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_rat = self.post_set.aggregate(p_rating=Sum('post_rating'))
        p_rat = 0
        p_rat += post_rat.get('p_rating')

        comment_rat = self.user.comment_set.aggregate(c_rating=Sum('comment_rating'))
        c_rat = 0
        c_rat += comment_rat.get('c_rating')

        post_author = self.post_set.all()
        sum_rating_comment_post_author = sum(
            [x['comment_rating'] for x in Comment.objects.filter(post__in=post_author).values()])

        self.user_rating = p_rat * 3 + c_rat + sum_rating_comment_post_author
        self.save()

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    topic_name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, )

    def __str__(self):
        return f'{self.topic_name}'


class Post(models.Model):
    article = 'AR'
    news = 'NE'
    TYPES = [
        (article, 'статья'),
        (news, 'новость')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPES, default=article)
    release_date = models.DateTimeField(auto_now_add=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        preview_text = f'{self.post_text[:124]}...'
        return preview_text

    def __str__(self):
        return (f'{self.author}\n {self.type}\n {self.release_date}\n {self.categories.all()}\n '
                f'{self.title}\n {self.post_text}\n {self.post_rating}')

    def get_absolute_url(self):
        return f'/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default="Нет комментария")
    create_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
