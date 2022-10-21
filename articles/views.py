from django.shortcuts import render, redirect

# Create your views here.
def detail(request, pk):
    article = Article.objects.get(id=pk)
    context = {
        "article": article,
    }
    return render(request, "articles/detail.html", context)


def detail(request, pk):
    article = Article.objects.get(id=pk)
    article.delete()
    return redirect("articles:index")
