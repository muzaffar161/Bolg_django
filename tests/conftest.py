import pytest
from django.contrib.auth.models import User

from blog.models import Article, Category, Comment, Tag


@pytest.fixture(autouse=True)
def _skip_turnstile_verification(monkeypatch):
    monkeypatch.setattr(
        "dj_turnstile.fields.TurnstileField.clean",
        lambda self, value: value,
    )


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice",
        email="alice@example.com",
        password="test-password-123",
        first_name="Alice",
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username="bob",
        email="bob@example.com",
        password="test-password-123",
    )


@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Cinema",
        description="Stories about film.",
        accent="#f59e0b",
    )


@pytest.fixture
def tag(db):
    return Tag.objects.create(name="review")


@pytest.fixture
def article(db, user, category, tag):
    item = Article.objects.create(
        author=user,
        category=category,
        title="A great movie night",
        excerpt="Why this film still matters.",
        body="First paragraph.\n\nSecond paragraph with a few more words.",
        status=Article.STATUS_PUBLISHED,
    )
    item.tags.add(tag)
    return item


@pytest.fixture
def draft_article(db, user, category):
    return Article.objects.create(
        author=user,
        category=category,
        title="Unfinished notes",
        excerpt="Work in progress.",
        body="To be continued.",
        status=Article.STATUS_DRAFT,
    )


@pytest.fixture
def comment(db, article, other_user):
    return Comment.objects.create(
        article=article,
        author=other_user,
        body="What a thoughtful review.",
    )
