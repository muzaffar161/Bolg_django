from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"articles", views.ArticleViewSet, basename="api-article")
router.register(r"categories", views.CategoryViewSet, basename="api-category")
router.register(r"comments", views.CommentViewSet, basename="api-comment")

urlpatterns = [
    path("", views.home, name="home"),
    path("articles/", views.article_list, name="article_list"),
    path("articles/cbv/", views.ArticleListView.as_view(), name="article_list_cbv"),
    path("articles/add/", views.add_article, name="add_article"),
    path("articles/<int:id>/", views.article_detail, name="article_detail"),
    path(
        "articles/<int:id>/edit/",
        views.ArticleUpdateView.as_view(),
        name="edit_article",
    ),
    path(
        "articles/<int:id>/delete/",
        views.ArticleDeleteView.as_view(),
        name="delete_article",
    ),
    path("articles/<int:id>/comments/", views.add_comment, name="add_comment"),
    path("categories/", views.category_list, name="category_list"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("tag/<slug:slug>/", views.tag_detail, name="tag_detail"),
    path("authors/<int:id>/", views.author_detail, name="author_detail"),
    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("api/", include(router.urls)),
]
