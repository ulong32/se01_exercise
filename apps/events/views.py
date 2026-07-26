from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_datetime

from .models import Category, Event
from .services import create_event, delete_event, update_event

User = get_user_model()


def home(request):
    return render(request, "events/home.html")


def event_list(request):
    query = request.GET.get("q", "")
    if query:
        events = Event.objects.filter(title__icontains=query)
    else:
        events = Event.objects.all()

    if request.headers.get("HX-Request"):
        return render(request, "events/_event_results.html", {"events": events})
    return render(request, "events/event_list.html", {"events": events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, "events/event_detail.html", {"event": event})


@login_required(login_url="/users/login/")
def event_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date_str = request.POST.get("date")
        location = request.POST.get("location")
        category_id = request.POST.get("category_id")

        if not all([title, description, date_str, location, category_id]):
            return HttpResponseBadRequest("Missing required fields")

        creator = request.user

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return HttpResponseBadRequest("Invalid category selected.")

        parsed_date = parse_datetime(date_str)
        if parsed_date is None:
            return HttpResponseBadRequest(
                "Invalid date format; expected ISO 8601 datetime"
            )

        event = create_event(
            title=title,
            description=description,
            date=parsed_date,
            location=location,
            category=category,
            creator=creator,
        )
        return redirect("events:event_detail", event_id=event.id)
    else:
        categories = Category.objects.all()
        return render(request, "events/event_create.html", {"categories": categories})


@login_required(login_url="/users/login/")
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if not (
        request.user == event.creator
        or request.user.is_superuser
        or request.user.is_staff
    ):
        return HttpResponseForbidden("You do not have permission to edit this event.")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date_str = request.POST.get("date")
        location = request.POST.get("location")
        category_id = request.POST.get("category_id")

        if not all([title, description, date_str, location, category_id]):
            return HttpResponseBadRequest("Missing required fields")

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return HttpResponseBadRequest("Invalid category selected.")

        parsed_date = parse_datetime(date_str)
        if parsed_date is None:
            return HttpResponseBadRequest(
                "Invalid date format; expected ISO 8601 datetime"
            )

        update_event(
            event,
            title=title,
            description=description,
            date=parsed_date,
            location=location,
            category=category,
        )
        return redirect("events:event_detail", event_id=event.id)
    else:
        categories = Category.objects.all()
        return render(
            request,
            "events/event_edit.html",
            {"event": event, "categories": categories},
        )


@login_required(login_url="/users/login/")
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if not (
        request.user == event.creator
        or request.user.is_superuser
        or request.user.is_staff
    ):
        return HttpResponseForbidden("You do not have permission to delete this event.")

    if request.method == "POST":
        delete_event(event)
        return redirect("events:event_list")
    else:
        return HttpResponseBadRequest("Only POST requests are allowed for deletion.")
