from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from django.contrib import messages
from .models import Article, Comment

# Create your views here.


def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        _articles = Article.objects.filter(title__contains=keyword)
        return render(request, "articles.html", {"articles": _articles})

    articles_ = Article.objects.all()
    return render(request, "articles.html", {"articles": articles_})


def index(request):
    context = {"numbers": [1, 2, 3, 4, 5, 6]}
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    context = {
        "articles": articles
    }
    return render(request, "dashboard.html", context)


@login_required(login_url="user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        # form.save = 1-article objesi -> 2-article.save()
        article.author = request.user
        article.save()

        messages.success(request, "Makale başarıyla oluşturuldu")
        return redirect("article:dashboard")

    return render(request, "addarticle.html", {"form": form})


def detail(request, id):
    # article = Article.objects.filter(id=id).first()
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()

    return render(request, "details.html", {"article": article, "comments": comments})


@login_required(login_url="user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()

        messages.success(request, "Makale Başarıyla Güncellendi")
        return redirect("article:dashboard")

    return render(request, "update.html", {"form": form, "author": article.author, "user": request.user})


@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, "Makale Başarıyla Silindi")
    return redirect("article:dashboard")


@login_required(login_url="user:login")
def addComment(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author=request.user, comment_content=comment_content)
        newComment.article = article
        newComment.save()

    return redirect(reverse("article:detail", kwargs={"id": id}))  # /articles/detail/15





