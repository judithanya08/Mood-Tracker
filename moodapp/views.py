from django.shortcuts import render, redirect, get_object_or_404 
from .models import MoodEntry
from .forms import MoodEntryForm
from django.db.models import Count
from datetime import date
import calendar


# Create your views here.
def home(request):
    return render(request, 'home.html')

def add_mood(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_history')
    else:
        form = MoodEntryForm()
    return render(request, 'add_mood.html', {'form':form})

def view_history(request):
    entries = MoodEntry.objects.all().order_by('-date')
    return render(request, 'view_history.html', {'entries': entries})

def edit_mood(request, entry_id):
    # Find the mood entry by its ID or show 404 if it doesn't exist
    entry = get_object_or_404(MoodEntry, id=entry_id)

    #if form was submitted, update the entry with new data
    if request.method == 'POST':
        form = MoodEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('view_history')
    else:
        form = MoodEntryForm(instance=entry)

    return render(request, 'edit_mood.html', {'form': form})

def delete_mood(request, entry_id):
    #find the mood entry by its ID
    entry = get_object_or_404(MoodEntry, id=entry_id)

    if request.method == 'POST':
        #if user confirmed deletion, delete and go back to history
        entry.delete()
        return redirect('view_history')

    #if it's GET, show a confirmation page
    return render(request, 'delete_mood.html', {'entry': entry})

def mood_trends(request):
    # Group entries by mood and count how many times each mood appears
    mood_counts = (
        MoodEntry.objects.values('mood')
        .annotate(total=Count('mood'))
        .order_by('-total')
    )
    return render(request, 'mood_trends.html', {'mood_counts': mood_counts})

def mood_calendar(request):
    # Use today's date as the default month/year
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # Build a calendar for this month (weeks of date objects)
    cal = calendar.Calendar(firstweekday=6)  # 6 = Sunday start, 0 = Monday start
    weeks = cal.monthdatescalendar(year, month)

    # Get all entries for this month
    month_entries = MoodEntry.objects.filter(date__year=year, date__month=month)
    dates_with_entries = {entry.date for entry in month_entries}

    # For display purposes (month name like "December")
    month_name = calendar.month_name[month]

    context = {
        'year': year,
        'month': month,
        'month_name': month_name,
        'weeks': weeks,
        'dates_with_entries': dates_with_entries,
    }
    return render(request, 'mood_calendar.html', context)
