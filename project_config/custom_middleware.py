from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated and not any(path in request.path for path in ["login", "logout", "signup", "admin"]):
            return redirect(reverse("login"))
        return response
