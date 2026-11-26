import pytest

from blog.models import Article


@pytest.mark.django_db
def test_api_article_list_is_public(client, article):
    response = client.get("/api/articles/")

    assert response.status_code == 200
    assert response.json()[0]["title"] == "A great movie night"


@pytest.mark.django_db
def test_api_article_detail(client, article):
    response = client.get(f"/api/articles/{article.id}/")

    assert response.status_code == 200
    assert response.json()["author_name"] == "alice"
    assert response.json()["category_name"] == "Cinema"


@pytest.mark.django_db
def test_api_category_list(client, category):
    response = client.get("/api/categories/")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Cinema"


@pytest.mark.django_db
def test_api_article_create_requires_authentication(client, category):
    response = client.post(
        "/api/articles/",
        {
            "title": "API story",
            "category": category.id,
            "excerpt": "Short text.",
            "body": "Full text.",
            "status": Article.STATUS_PUBLISHED,
        },
        content_type="application/json",
    )

    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_api_authenticated_user_creates_article(client, user, category):
    client.force_login(user)

    response = client.post(
        "/api/articles/",
        {
            "title": "API story",
            "category": category.id,
            "excerpt": "Short text.",
            "body": "Full text.",
            "status": Article.STATUS_PUBLISHED,
        },
        content_type="application/json",
    )

    assert response.status_code == 201
    assert response.json()["author_name"] == "alice"
    assert Article.objects.filter(title="API story").exists()


@pytest.mark.django_db
def test_api_comment_list(client, comment):
    response = client.get("/api/comments/")

    assert response.status_code == 200
    assert response.json()[0]["body"] == "What a thoughtful review."
