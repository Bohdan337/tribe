from django.shortcuts import render, redirect
from .forms import ScheduleForm
from django.http import JsonResponse
from django.template.loader import render_to_string

def create_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save()
            html = render_to_string('course/schedule_template.html', {'schedule': schedule})

            return JsonResponse({'status': 'success', 'html': html})
    
    return JsonResponse({'status': 'failed', 'error': 'invalid request'}), 400
