from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

User = get_user_model()


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(
                request,
                "users/user_register.html",
                {"error": "Missing username or password"},
                status=400,
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "users/user_register.html",
                {"error": "Username already exists"},
                status=400,
            )

        User.objects.create_user(username=username, password=password)
        return redirect("/")
    else:
        return render(request, "users/user_register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(
                request,
                "users/login.html",
                {"error": "Invalid username or password"},
                status=400,
            )
    else:
        return render(request, "users/login.html")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("/")
