from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, View

from backend.tokens.models import Token, TokenRound

from .forms import AvatarUpdateForm, BuyTokenForm, ProfileUserUpdateForm

User = get_user_model()


class HomeRedirectView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(
                reverse("dashboard:index", kwargs={"username": request.user.username}),
                permanent=False,
            )
        return redirect(reverse("account_login"), permanent=False)


class DashboardRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            "dashboard:index", kwargs={"username": self.request.user.username}
        )


class DashboardIndexView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["token"] = Token.objects.first()
        context["token_rounds"] = TokenRound.objects.all()
        return context


class DashboardTokenView(LoginRequiredMixin, View):
    template_name = "dashboard/token.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        buy_token_form = BuyTokenForm()
        token = Token.objects.first()
        token_rounds = TokenRound.objects.all()
        context = {
            "user": user,
            "token": token,
            "token_rounds": token_rounds,
            "buy_token_form": buy_token_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = BuyTokenForm(request.POST)
        if form.is_valid():
            # token_amount = form.cleaned_data['token_amount']
            # token_price_usdt = form.cleaned_data['token_price_usdt']
            return redirect(
                reverse(
                    "dashboard:token", kwargs={"username": self.request.user.username}
                )
            )
        user = self.request.user
        context = {"user": user, "buy_token_form": form}
        return render(request, self.template_name, context)


class DashboardTeamView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "dashboard/team.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["token"] = Token.objects.first()
        return context


class DashboardProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProfileUserUpdateForm
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "dashboard/profile.html"
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse(
            "dashboard:profile", kwargs={"username": self.request.user.username}
        )

    def get_object(self, *args, **kwargs):
        return self.request.user


class AvatarUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        form = AvatarUpdateForm(request.POST, request.FILES)
        if form.is_valid() and request.FILES:
            user = self.request.user
            user.avatar = form.cleaned_data.get("avatar")
            user.save()
            return JsonResponse({"avatar_url": user.avatar.url})
        # handle form errors
        errors = form.errors.as_data()
        error_messages = [
            error.message for error_list in errors.values() for error in error_list
        ]
        return JsonResponse({"error": error_messages}, status=400)
