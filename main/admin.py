from django.contrib import admin

from django.db.models import ManyToManyField, ForeignKey

from .models import Post, Like, Comment

class LikeInline(admin.TabularInline):

    model = Post.likes.through


class CommentInline(admin.TabularInline):

    model = Post.comments.through


class PostAdmin(admin.ModelAdmin):

    inlines = [
        LikeInline,
        CommentInline,
        ]

    list_display = [field.name for field in Post._meta.fields]
    fields = [field.name for field in Post._meta.fields if field.name not in ["id"]]


class LikeAdmin(admin.ModelAdmin):

    list_display = [field.name for field in Like._meta.fields]
    fields = [field.name for field in Like._meta.fields if field.name not in ["id"]]


class CommentAdmin(admin.ModelAdmin):

    list_display = [field.name for field in Comment._meta.fields]
    fields = [field.name for field in Comment._meta.fields if field.name not in ["id"]]


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
