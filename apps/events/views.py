from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import Event, Category

User = get_user_model()

def home(request):
    return HttpResponse("Welcome to the Event Listings Web Application!")

def event_list(request):
    events = Event.objects.all()
    if not events.exists():
        return HttpResponse("No events available at this time.")
    
    event_data = [
        {"id": event.id, "title": event.title, "date": str(event.date), "location": event.location}
        for event in events
    ]
    return JsonResponse({"events": event_data})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return JsonResponse({
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "date": str(event.date),
        "location": event.location,
        "category": event.category.name,
        "creator": event.creator.username
    })

# NOTE: CSRF is exempted only for this early stub endpoint; remove once real forms/auth are added.
@csrf_exempt
def event_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date_str = request.POST.get("date")
        location = request.POST.get("location")
        category_id = request.POST.get("category_id")

        if not all([title, description, date_str, location, category_id]):
            return HttpResponseBadRequest("Missing required fields")

        # Hard-coded creator for now
        creator = User.objects.first()
        if not creator:
            # Fallback if no user exists
            creator = User.objects.create_user(username="default_creator", password="password")

        category = get_object_or_404(Category, pk=category_id)

        from django.utils.dateparse import parse_datetime

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
        return HttpResponseRedirect(f"/events/{event.id}/")
    else:
        return HttpResponse("Event creation form placeholder. Send POST request here to create an event.")
