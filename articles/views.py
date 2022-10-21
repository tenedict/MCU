from django.shortcuts import render, redirect
from accounts.forms import MyUserChangeForm
from .models import Review, Comment
from .forms import ReviewForm, CommentForm

# Create your views here.
def index(request):
    reviews = Review.objects.order_by("-id")
    context = {"reviews": reviews}
    return render(request, "articles/index.html", context)


def create(request):
    if request.method == "POST":
        # DB에 저장하는 로직
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit = False)
            review.user = request.user
            review_form.save()
            return redirect("articles:index")
    else:
        review_form = ReviewForm()
    context = {"review_form": review_form}
    return render(request, "articles/create.html", context=context)


def detail(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = review
            comment.user = request.user
            comment.save()
        return redirect('articles:detail', review.pk)
    else:
        comment_form = CommentForm()
    context = {
        "comment_form": comment_form,
        "review" : review,
    }
    return render(request, "articles/detail.html", context)


def delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect("articles:index")

def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review,)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', review.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form': form
    }
    return render(request, 'articles/update.html', context=context)

def comment_delete(request, pk, comment_pk):
    article = Review.objects.get(pk=pk)
    if request.user == article.user:
        Comment.objects.get(pk=comment_pk).delete()
        return redirect('articles:detail', pk)
    else:
        return redirect('articles:detail', pk)

# 에러 처리

def error_400(request, exception):
    return render(request, "400.html", status=400)


def error_403(request, exception):
    return render(request, "403.html", status=403)


def error_404(request, exception):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)
