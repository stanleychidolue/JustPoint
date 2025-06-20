from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.views import PasswordChangeView, LoginView, PasswordResetView
from Cart.models import Cart, CartItems
from .forms import CustomUserRegisterForm, UpdatePasswordForm, UpdateUserInfoForm
from django.contrib import messages
from User.models import CustomUser
from typing import Any
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class MyLoginView(LoginView):

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        response = super().form_valid(form)
        # form.cleaned_data.get("remember_me")
        if self.request.POST.get("remember_me"):
            self.request.session.set_expiry(604800)
        else:
            # This part of code means, close session when browser is closed.
            self.request.session.set_expiry(0)
        return response

    def get_success_url(self) -> str:
        response = super().get_success_url()
        try:
            session_cart = Cart.objects.get(
                session_id=self.request.session.get('session_id'), paid=False)
            if Cart.objects.filter(user=self.request.user, paid=False).exists():
                user_cart = Cart.objects.get(
                    user=self.request.user, paid=False)
                user_cart_prod = [
                    item.product for item in user_cart.cartitems.all()]
                for item in session_cart.cartitems.all():
                    if not item.product in user_cart_prod:
                        cart_items = CartItems(
                            cart=user_cart, product=item.product, quantity=item.quantity)
                        cart_items.save()
                if session_cart != user_cart:
                    session_cart.delete()
            else:
                session_cart.user = self.request.user
                session_cart.delivery_address = self.request.user.address
                session_cart.session_id = None
                session_cart.save()
        except:
            pass
        return response


def register_page(request):
    form = CustomUserRegisterForm()
    if request.method == "POST":
        form = CustomUserRegisterForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Your account has been created")
            return redirect("login-page")
        form = CustomUserRegisterForm(request.POST)

    return render(request, "user/register.html", {"form": form})


class MyPasswordResetView(PasswordResetView):

    def form_valid(self, form: Any) -> HttpResponse:
        response = super().form_valid(form)
        # email=self.request.POST.get("email")
        email = form.cleaned_data["email"]
        if CustomUser.objects.filter(email=email).exists():
            return response
        else:
            messages.add_message(self.request, messages.WARNING,
                                 "The email provided is not valid, please confirm your email")
            return super().form_invalid(form)


@login_required
def user_profile(request, option: str = None):
    arguement = {}
    if option == "edit":
        form = UpdateUserInfoForm(instance=request.user)
        arguement = {"form": form, "edit": True}
    elif option == "delete_account":
        arguement = {"delete_account": True}

    elif option == "order-history":
        order_history = Cart.objects.filter(
            user=request.user, paid=True).order_by("-date")
        arguement = {"order_history": True, "processed_orders": order_history}
    elif type(option) == str:
        cart_items = CartItems.objects.filter(cart_id=option)
        arguement = {"order_history": True,
                     "specific_order": True, "cart_items": cart_items}
    else:
        arguement = {"my_details": True}

    if request.method == "POST":
        if option == "edit":
            form = UpdateUserInfoForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.add_message(
                    request, messages.SUCCESS, "Your details has been updated sucessfully")
                return redirect("user-profile")
        elif option == "delete_account":
            user = request.user
            user.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "Your Account has been deleted successfully")
            return redirect("login-page")
    return render(request, "user/profile.html", arguement)


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    success_message = 'Your password has been changed successfully'
    template_name = "user/profile.html"
