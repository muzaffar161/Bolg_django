import pytest

from blog.models import Article, Category, Comment, Tag


@pytest.mark.django_db
def test_category_slug_is_generated():
    category = Category.objects.create(name="Sport & Culture")

    assert category.slug == "sport-culture"
    assert str(category) == "Sport & Culture"


@pytest.mark.django_db
def test_tag_slug_is_generated():
    tag = Tag.objects.create(name="Behind The Scenes")

    assert tag.slug == "behind-the-scenes"
    assert str(tag) == "Behind The Scenes"


@pytest.mark.django_db
def test_article_creation(article, user, category, tag):
    assert article.author == user
    assert article.category == category
    assert article.status == Article.STATUS_PUBLISHED
    assert article.published_at is not None
    assert list(article.tags.all()) == [tag]
    assert str(article) == "A great movie night"


@pytest.mark.django_db
def test_article_slug_is_unique(user, category):
    first = Article.objects.create(
        author=user,
        category=category,
        title="Same title",
        excerpt="First story.",
        body="Body one.",
    )
    second = Article.objects.create(
        author=user,
        category=category,
        title="Same title",
        excerpt="Second story.",
        body="Body two.",
    )

    assert first.slug != second.slug
    assert second.slug.startswith("same-title")


@pytest.mark.django_db
def test_draft_has_no_publication_date(draft_article):
    assert draft_article.status == Article.STATUS_DRAFT
    assert draft_article.published_at is None


@pytest.mark.django_db
def test_article_relationships(article, comment):
    assert article.comments.count() == 1
    assert comment.article == article
    assert article.comment_count == 1
    assert article.category.articles.count() == 1
    assert str(comment) == "bob on A great movie night"


@pytest.mark.django_db
def test_only_approved_comments_are_counted(article, comment):
    comment.is_approved = False
    comment.save()

    assert article.comment_count == 0


@pytest.mark.django_db
def test_author_profile_created_by_signal(user):
    assert user.author_profile is not None
    assert user.author_profile.user == user


@pytest.mark.django_db
def test_reading_time(article):
    assert article.reading_time == 1

    article.body = " ".join(["word"] * 450)
    article.save()

    assert article.reading_time == 2
