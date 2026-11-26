import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from blog.models import Article, Comment


@pytest.mark.django_db
def test_home_page(client, article):
    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert b"A great movie night" in response.content


@pytest.mark.django_db
def test_article_list_page(client, article):
    response = client.get(reverse("article_list"))

    assert response.status_code == 200
    assert b"A great movie night" in response.content


@pytest.mark.django_db
def test_class_based_list_page(client, article):
    response = client.get(reverse("article_list_cbv"))

    assert response.status_code == 200
    assert b"A great movie night" in response.content


@pytest.mark.django_db
def test_article_detail_page(client, article):
    response = client.get(reverse("article_detail", args=[article.id]))

    assert response.status_code == 200
    assert b"First paragraph." in response.content

    article.refresh_from_db()
    assert article.views == 1


@pytest.mark.django_db
def test_article_detail_not_found(client):
    response = client.get(reverse("article_detail", args=[99999]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_search_filters_articles(client, article):
    response = client.get(reverse("article_list"), {"q": "movie"})

    assert response.status_code == 200
    assert b"A great movie night" in response.content

    response = client.get(reverse("article_list"), {"q": "hockey"})

    assert b"A great movie night" not in response.content


@pytest.mark.django_db
def test_category_and_tag_pages(client, article, category, tag):
    assert client.get(category.get_absolute_url()).status_code == 200
    assert client.get(reverse("tag_detail", args=[tag.slug])).status_code == 200
    assert client.get(reverse("category_list")).status_code == 200


@pytest.mark.django_db
def test_static_pages(client):
    assert client.get(reverse("about")).status_code == 200
    assert client.get(reverse("register")).status_code == 200
    assert client.get(reverse("login")).status_code == 200
    assert b"cf-turnstile" in client.get(reverse("login")).content


@pytest.mark.django_db
def test_draft_is_hidden_from_list(client, draft_article):
    response = client.get(reverse("article_list"))

    assert b"Unfinished notes" not in response.content


@pytest.mark.django_db
def test_add_article_requires_login(client):
    response = client.get(reverse("add_article"))

    assert response.status_code == 302
    assert reverse("login") in response.url


@pytest.mark.django_db
def test_logged_in_user_can_add_article(client, user, category):
    client.force_login(user)

    response = client.post(
        reverse("add_article"),
        {
            "title": "A fresh take on derby day",
            "category": category.id,
            "excerpt": "Short introduction.",
            "body": "The full article body goes here.",
            "status": Article.STATUS_PUBLISHED,
        },
    )

    assert response.status_code == 302
    assert Article.objects.filter(title="A fresh take on derby day").exists()


@pytest.mark.django_db
def test_other_user_cannot_edit_article(client, other_user, article):
    client.force_login(other_user)

    response = client.get(reverse("edit_article", args=[article.id]))

    assert response.status_code == 403


@pytest.mark.django_db
def test_author_can_edit_article(client, user, article):
    client.force_login(user)

    response = client.get(reverse("edit_article", args=[article.id]))

    assert response.status_code == 200


@pytest.mark.django_db
def test_add_comment(client, other_user, article):
    client.force_login(other_user)

    response = client.post(
        reverse("add_comment", args=[article.id]),
        {"body": "Thanks for sharing this perspective."},
    )

    assert response.status_code == 302
    assert Comment.objects.filter(article=article, author=other_user).exists()


@pytest.mark.django_db
def test_register_creates_user(client):
    response = client.post(
        reverse("register"),
        {
            "username": "newreader",
            "email": "newreader@example.com",
            "password1": "Sup3rSecret!Pass",
            "password2": "Sup3rSecret!Pass",
        },
    )

    assert response.status_code == 302
    assert User.objects.filter(username="newreader").exists()


@pytest.mark.django_db
def test_profile_is_protected(client, user):
    assert client.get(reverse("profile")).status_code == 302

    client.force_login(user)

    assert client.get(reverse("profile")).status_code == 200
