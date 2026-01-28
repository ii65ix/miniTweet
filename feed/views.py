from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignUpForm, TweetForm
from .models import Tweet


def home(request):
    tweets = Tweet.objects.select_related("author")
    form = TweetForm()
    return render(
        request,
        "feed/home.html",
        {
            "tweets": tweets,
            "form": form,
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
    tweets = Tweet.objects.filter(author=request.user)
    return render(
        request,
        "feed/profile.html",
        {
            "tweets": tweets,
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
