from django.shortcuts import render, redirect
from .forms import ScheduleForm

def create_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = ScheduleForm()
    return render(request, 'courses/create_schedule.html', {'form': form})
