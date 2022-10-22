from .forms import ArticleForm, CommentForm, MiniCommentForm
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .models import Article, Comment, Like
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def reviews(request):
    articles = Article.objects.order_by("-id")
    context = {
        "articles": articles,
    }
    return render(request, "articles/reviews.html", context)


@login_required
def create(request):
    user = request.user
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = user
            article.save()
            messages.success(request, "작성하였습니다.")
            return redirect("articles:reviews")
    else:
        form = ArticleForm()
    context = {
        "form": form,
    }
    return render(request, "articles/form.html", context)


def search(request):
    if request.method == "POST":
        search = request.POST["search"]
        searched_users = get_user_model().objects.filter(username__contains=search)
        searched_articles = Article.objects.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(movie_name__icontains=search)
        )
        context = {
            "search": search,
            "searched_users": searched_users,
            "searched_articles": searched_articles,
        }
        return render(request, "articles/reviews.html", context)


def detail(request, pk):
    if request.user.is_authenticated:
        user_recommends = request.user.like_set.all()
        try:
            flag = user_recommends.get(article_id=pk)
        except:
            flag = 0
        target_article = Article.objects.get(id=pk)
        like_ = Like.objects.filter(article=target_article)
        like_length = len(like_)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = target_article
                comment.user = request.user
                comment.save()
                messages.success(request, "작성하였습니다.")
                return redirect("articles:detail", target_article.pk)
        else:
            form = CommentForm()
        context = {
            "flag": flag,
            "article": target_article,
            "like_length": like_length,
            "like_": like_,
            "form": form,
        }

        response = render(request, "articles/detail.html", context)

        # 조회수
        # expire_date, now = datetime.now(), datetime.now()
        # expire_date += timedelta(days=1)
        # expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
        # expire_date -= now
        # max_age = expire_date.total_seconds()
        # cookie_value = request.COOKIES.get("hitboard", "_")
        # if not f"_{pk}_" in cookie_value:
        #     cookie_value += f"{pk}_"
        #     response.set_cookie(
        #         "hitboard", value=cookie_value, max_age=max_age, httponly=True
        #     )

        target_article.view += 1
        target_article.save()
        return response
    else:
        target_article = Article.objects.get(id=pk)
        like_ = Like.objects.filter(article=target_article)
        like_length = len(like_)
        context = {
            "article": target_article,
            "like_length": like_length,
            "like_": like_,
        }
        target_article.view += 1
        target_article.save()
        return render(request, "articles/detail.html", context)


@login_required
def update(request, pk):
    user = request.user
    like_ = Like.objects.all()
    article = Article.objects.get(id=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "수정되었습니다.")
            return redirect("articles:detail", article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        "form": form,
        "user": user,
        "like_": like_,
        "article": article,
    }
    return render(request, "articles/form.html", context)


@login_required
def delete(request, pk):
    article = Article.objects.get(id=pk)
    user = request.user
    if request.method == "POST":
        article.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect("articles:reviews")
    context = {
        "article": article,
        "user": user,
    }
    return render(request, "articles/delete.html", context)


@login_required
def comment_update(request, article_pk, comment_pk):
    form = CommentForm()
    user_recommends = request.user.like_set.all()
    try:
        flag = user_recommends.get(article_id=article_pk)
    except:
        flag = 0
    user = request.user
    article = Article.objects.get(id=article_pk)
    like_ = Like.objects.filter(article=article)
    like_length = len(like_)
    target_comment = Comment.objects.get(id=comment_pk)
    if user.pk == target_comment.user.pk:
        if request.method == "POST":
            comment_form = MiniCommentForm(request.POST, instance=target_comment)
            if comment_form.is_valid():
                comment_form.save()
                messages.success(request, "수정되었습니다.")
                return redirect("articles:detail", article.pk)
        else:
            comment_form = MiniCommentForm(instance=target_comment)
        context = {
            "flag": flag,
            "like_length": like_length,
            "target_comment": target_comment,
            "article": article,
            "form": form,
            "comment_form": comment_form,
            "user": user,
        }
        return render(request, "articles/detail.html", context)
    else:
        messages.warning(request, "권한이 없습니다.")
        return redirect("articles:detail", article_pk)


@login_required
def comment_delete(request, article_pk, comment_pk):
    user = request.user
    comment = Comment.objects.get(id=comment_pk)
    if user.pk == comment.user.pk:
        comment.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect("articles:detail", article_pk)
    else:
        messages.warning(request, "권한이 없습니다.")
        return redirect("articles:detail", article_pk)


@login_required
def add_like(request, pk):
    target_article = Article.objects.get(id=pk)
    target_user = request.user
    try:
        if target_article.like_set.get(user=target_user):
            like_ = Like.objects.filter(user=target_user, article=target_article)
            like_.delete()
            return redirect("articles:detail", target_article.pk)
        else:
            like_ = Like.objects.create(article=target_article, user=target_user)
            like_.save()
            return redirect("articles:detail", target_article.pk)
    except:
        like_ = Like.objects.create(article=target_article, user=target_user)
        like_.save()
        messages.success(request, "추천!")
        return redirect("articles:detail", target_article.pk)


# 에러 처리


def error_400(request, exception):
    return render(request, "400.html", status=400)


def error_403(request, exception):
    return render(request, "403.html", status=403)


def error_404(request, exception):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)
