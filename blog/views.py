from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, ListView, UpdateView
from rest_framework import permissions, viewsets

from .forms import (
    ArticleForm,
    AuthorProfileForm,
    CommentForm,
    LoginWithTurnstileForm,
    RegisterForm,
)
from .models import Article, AuthorProfile, Category, Comment, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    ArticleSerializer,
    CategorySerializer,
    CommentSerializer,
)

ARTICLES_PER_PAGE = 6


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = (
        Article.objects.select_related("author", "category")
        .prefetch_related("tags")
        .all()
    )
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "article").all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


def _published_articles():
    return (
        Article.objects.filter(status=Article.STATUS_PUBLISHED)
        .select_related("author", "category")
        .prefetch_related("tags")
    )


def _filter_articles(request, queryset):
    search = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    tag_slug = request.GET.get("tag", "").strip()

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(excerpt__icontains=search)
            | Q(body__icontains=search)
        )
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)
    if tag_slug:
        queryset = queryset.filter(tags__slug=tag_slug).distinct()

    return queryset, search, category_slug, tag_slug


def _list_context(request, queryset=None):
    articles = queryset if queryset is not None else _published_articles()
    articles, search, category_slug, tag_slug = _filter_articles(request, articles)
    page = Paginator(articles, ARTICLES_PER_PAGE).get_page(request.GET.get("page"))

    return {
        "page_obj": page,
        "articles": page.object_list,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "featured": _published_articles().filter(is_featured=True)[:3],
        "search": search,
        "selected_category": category_slug,
        "selected_tag": tag_slug,
    }


def home(request):
    context = _list_context(request)
    context["total_articles"] = _published_articles().count()
    context["lead_article"] = context["featured"][0] if context["featured"] else None
    return render(request, "blog/home.html", context)


def article_list(request):
    return render(request, "blog/article_list.html", _list_context(request))


class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"
    paginate_by = ARTICLES_PER_PAGE

    def get_queryset(self):
        queryset, _, _, _ = _filter_articles(self.request, _published_articles())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "categories": Category.objects.all(),
                "tags": Tag.objects.all(),
                "featured": _published_articles().filter(is_featured=True)[:3],
                "search": self.request.GET.get("q", "").strip(),
                "selected_category": self.request.GET.get("category", "").strip(),
                "selected_tag": self.request.GET.get("tag", "").strip(),
                "cbv_mode": True,
            }
        )
        return context


def article_detail(request, id):
    Article.objects.filter(pk=id).update(views=F("views") + 1)

    article = get_object_or_404(
        _published_articles().prefetch_related("comments__author"),
        id=id,
    )

    return render(
        request,
        "blog/article_detail.html",
        {
            "article": article,
            "comments": article.comments.filter(is_approved=True),
            "comment_form": CommentForm(),
            "related": _published_articles()
            .filter(category=article.category)
            .exclude(pk=article.pk)[:3],
        },
    )


def category_list(request):
    return render(
        request,
        "blog/category_list.html",
        {"categories": Category.objects.all()},
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = _published_articles().filter(category=category)
    context = _list_context(request, articles)
    context["category"] = category
    return render(request, "blog/category_detail.html", context)


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    articles = _published_articles().filter(tags=tag)
    context = _list_context(request, articles)
    context["tag"] = tag
    return render(request, "blog/article_list.html", context)


def author_detail(request, id):
    author = get_object_or_404(
        AuthorProfile.objects.select_related("user"),
        user_id=id,
    )
    articles = _published_articles().filter(author=author.user)

    return render(
        request,
        "blog/author_detail.html",
        {"author": author, "articles": articles},
    )


def about(request):
    team = AuthorProfile.objects.select_related("user")[:4]
    return render(request, "blog/about.html", {"team": team})


@login_required
def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()
            messages.success(request, "Story published successfully.")
            return redirect("article_detail", id=article.id)
    else:
        form = ArticleForm()

    return render(
        request,
        "blog/article_form.html",
        {"form": form, "form_title": "Write a new story"},
    )


class ArticleOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        article = self.get_object()
        return article.author_id == self.request.user.id or self.request.user.is_staff


class ArticleUpdateView(LoginRequiredMixin, ArticleOwnerMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog/article_form.html"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit story"
        return context

    def get_success_url(self):
        return reverse("article_detail", kwargs={"id": self.object.id})


class ArticleDeleteView(LoginRequiredMixin, ArticleOwnerMixin, DeleteView):
    model = Article
    template_name = "blog/article_confirm_delete.html"
    pk_url_kwarg = "id"

    def get_success_url(self):
        return reverse("article_list")


@require_POST
@login_required
def add_comment(request, id):
    article = get_object_or_404(Article, id=id, status=Article.STATUS_PUBLISHED)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.author = request.user
        comment.save()
        messages.success(request, "Your comment has been added.")

    return redirect("article_detail", id=article.id)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can log in now.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    author_profile, _ = AuthorProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = AuthorProfileForm(
            request.POST,
            request.FILES,
            instance=author_profile,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = AuthorProfileForm(instance=author_profile)

    return render(
        request,
        "blog/profile.html",
        {
            "form": form,
            "author": author_profile,
            "my_articles": request.user.articles.select_related("category")[:5],
            "my_comments": request.user.comments.select_related("article")[:5],
        },
    )


login_view = auth_views.LoginView.as_view(
    template_name="blog/login.html",
    authentication_form=LoginWithTurnstileForm,
)
logout_view = auth_views.LogoutView.as_view()
