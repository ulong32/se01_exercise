from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from .models import Event, Category
from django.utils.dateparse import parse_datetime

User = get_user_model()

def home(request):
    return render(request, 'events/home.html')

def event_list(request):
    query = request.GET.get('q', '')
    if query:
        events = Event.objects.filter(title__icontains=query)
    else:
        events = Event.objects.all()
    
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

def event_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date_str = request.POST.get("date")
        location = request.POST.get("location")
        category_id = request.POST.get("category_id")

        if not all([title, description, date_str, location, category_id]):
            return HttpResponseBadRequest("Missing required fields")

        if not request.user.is_authenticated:
            return HttpResponseBadRequest("You must be logged in to create an event.")
        
        creator = request.user

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return HttpResponseBadRequest("Invalid category selected.")

        parsed_date = parse_datetime(date_str)
        if parsed_date is None:
            return HttpResponseBadRequest("Invalid date format; expected ISO 8601 datetime")

        event = Event.objects.create(
            title=title,
            description=description,
            date=parsed_date,
            location=location,
            category=category,
            creator=creator,
        )
        return redirect(f"/events/{event.id}/")
    else:
        if not Category.objects.exists():
            Category.objects.create(name="Default")
        categories = Category.objects.all()
        return render(request, 'events/event_create.html', {'categories': categories})
