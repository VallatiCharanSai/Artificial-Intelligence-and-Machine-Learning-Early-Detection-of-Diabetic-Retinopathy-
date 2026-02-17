
from django.shortcuts import render, redirect
from .models import User
from django.core.files.storage import FileSystemStorage
from django.views.decorators.cache import never_cache
from myproject.ht import classify_dr
def register_view(request):
    msg = ""
    if request.method == "POST":
        uname = request.POST["username"]
        pwd = request.POST["password"]
        mail=request.POST["mail"]

        if User.objects.filter(mail=mail).exists():
            msg = "User already exists"
        else:
            User.objects.create(username=uname, password=pwd, mail=mail)
            return redirect("login")

    return render(request, "register.html", {"msg": msg})

@never_cache
def login_view(request):
    msg = ""
    if request.method == "POST":
        uname = request.POST["username"]
        pwd = request.POST["password"]

        try:
            user = User.objects.get(username=uname, password=pwd)
            request.session["user_id"] = user.id   # SESSION CREATED
            return redirect("dashboard")
        except:
            msg = "Wrong login details"

    return render(request, "login.html", {"msg": msg})

@never_cache
def dashboard(request):
    if "user_id" not in request.session:
        return redirect("login")
    user = User.objects.get(id=request.session["user_id"])
    return render(request, "dashboard.html",{"username":user.username})


def logout_view(request):
    request.session.flush()   # SESSION DESTROYED
    return redirect("login")
def profile(request):
    if "user_id" not in request.session:
        return redirect("login")
    user = User.objects.get(id=request.session["user_id"])
    return render(request, "profile.html",{"user":user})

def edit_profile(request):
    if "user_id" not in request.session:
        return redirect("login")

    user = User.objects.get(id=request.session["user_id"])
    msg = ""

    if request.method == "POST":
        user.username = request.POST["username"]
        user.mail = request.POST["mail"]
        user.save()
        msg = "Profile updated successfully"

    return render(request, "edit_profile.html", {"user": user, "msg": msg})
from myproject.gg import predict_image
# Load model ONCE (recommended)


def dr_prediction(request):
    context = {}

    if request.method == "POST" and request.FILES.get("image"):
        image_file = request.FILES["image"]

        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_path = fs.path(filename)

        idx, label = predict_image(image_path)

        context["image_url"] = fs.url(filename)
        context["prediction"] = f"{idx} - {label}"

    return render(request, "dr_prediction.html", context)