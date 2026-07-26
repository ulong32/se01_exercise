from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from .models import Event, Category
from django.utils.dateparse import parse_datetime
from .services import create_event

User = get_user_model()

def home(request):
    return render(request, 'events/home.html')

def event_list(request):
    query = request.GET.get('q', '')
    if query:
        events = Event.objects.filter(title__icontains=query)
    else:
        events = Event.objects.all()
    
    if request.headers.get('HX-Request'):
        return render(request, 'events/_event_results.html', {'events': events})
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required(login_url='/users/login/')
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
            return HttpResponseBadRequest("Invalid date format; expected ISO 8601 datetime")

        event = create_event(
            title=title,
            description=description,
            date=parsed_date,
            location=location,
            category=category,
            creator=creator,
        )
        return redirect('events:event_detail', event_id=event.id)
    else:
        categories = Category.objects.all()
        return render(request, 'events/event_create.html', {'categories': categories})
