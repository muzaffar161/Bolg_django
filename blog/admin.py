from django.contrib import admin

from .models import Article, AuthorProfile, Category, Comment, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "accent")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "category",
        "status",
        "is_featured",
        "views",
        "published_at",
    )
    search_fields = ("title", "excerpt", "body", "author__username")
    list_filter = ("status", "is_featured", "category", "tags")
    filter_horizontal = ("tags",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-published_at", "-created_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "article", "created_at", "is_approved")
    search_fields = ("body", "author__username", "article__title")
    list_filter = ("is_approved", "created_at")
    ordering = ("-created_at",)


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "website")
    search_fields = ("user__username", "user__email", "bio")
    ordering = ("user__username",)
