from rest_framework import serializers

from .models import Article, AuthorProfile, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    articles_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "accent",
            "articles_count",
        ]


class AuthorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = AuthorProfile
        fields = ["id", "username", "bio", "avatar", "website"]


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "author",
            "author_name",
            "category",
            "category_name",
            "tags",
            "excerpt",
            "body",
            "image",
            "status",
            "is_featured",
            "views",
            "created_at",
            "updated_at",
            "published_at",
            "comment_count",
        ]
        read_only_fields = [
            "author",
            "views",
            "created_at",
            "updated_at",
            "published_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "article",
            "author",
            "author_name",
            "body",
            "created_at",
            "is_approved",
        ]
        read_only_fields = ["author", "created_at"]
