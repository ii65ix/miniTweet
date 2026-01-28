from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignUpForm, TweetForm
from .models import Like, Tweet


def home(request):
    query = request.GET.get("q", "").strip()
    tweets = Tweet.objects.select_related("author").prefetch_related("likes")
    if query:
        tweets = tweets.filter(
            Q(content__icontains=query)
            | Q(author__username__icontains=query)
        )
    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(
            Like.objects.filter(user=request.user, tweet__in=tweets)
            .values_list("tweet_id", flat=True)
        )
    form = TweetForm()
    return render(
        request,
        "feed/home.html",
        {
            "tweets": tweets,
            "query": query,
            "form": form,
            "liked_ids": liked_ids,
        },
    )


@login_required
def create_tweet(request):
    if request.method != "POST":
        return redirect("home")

    form = TweetForm(request.POST)
    if form.is_valid():
        tweet = form.save(commit=False)
        tweet.author = request.user
        tweet.save()
    return redirect("home")


@login_required
def toggle_like(request, tweet_id):
    if request.method != "POST":
        return redirect("home")

    tweet = get_object_or_404(Tweet, id=tweet_id)
    like, created = Like.objects.get_or_create(
        user=request.user,
        tweet=tweet,
    )
    if not created:
        like.delete()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {
                "liked": created,
                "like_count": tweet.likes.count(),
            }
        )
    return redirect(request.POST.get("next") or "home")


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")


@login_required
def profile(request):
    tweets = (
        Tweet.objects.filter(author=request.user)
        .select_related("author")
        .prefetch_related("likes")
    )
    liked_ids = set(
        Like.objects.filter(user=request.user, tweet__in=tweets)
        .values_list("tweet_id", flat=True)
    )
    return render(
        request,
        "feed/profile.html",
        {
            "tweets": tweets,
            "liked_ids": liked_ids,
        },
    )


@login_required
def delete_account(request):
    if request.method != "POST":
        return redirect("profile")

    user = request.user
    logout(request)
    user.delete()
    return redirect("home")
