from django.db import models
from django.contrib.auth.models import User
from authorization.models import CustomUser



def directory_path(instance, filename):
    
    return '{0}/{1}'.format(instance.user.id, instance.id)


class Like(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return "%s"%(self.user)


class Comment(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    comment = models.TextField()

    def __str__(self):
        return "%s %s"%(self.user, self.comment)


class Post(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    body = models.TextField()
    image = models.FileField(upload_to=directory_path)
    likes = models.ManyToManyField(Like, related_name = 'likes', blank=True, null=True)
    comments = models.ManyToManyField(Comment, related_name = 'comments', blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "%s"%(self.title)