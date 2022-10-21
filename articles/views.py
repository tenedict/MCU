from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm

# Create your views here.
def index(request):
    reviews = Review.objects.order_by("-id")
    context = {"reviews": reviews}
    return render(request, "articles/index.html", context)


def create(request):
    if request.method == "POST":
        # DB에 저장하는 로직
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review_form.save()
            return redirect("articles:index")
    else:
        review_form = ReviewForm()
    context = {"review_form": review_form}
    return render(request, "articles/create.html", context=context)


def detail(request, pk):
    review = Review.objects.get(id=pk)
    context = {
        "review": review,
    }
    return render(request, "articles/detail.html", context)


def delete(request, pk):
    review = Review.objects.get(id=pk)
    review.delete()
    return redirect("articles:index")
