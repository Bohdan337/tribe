from django.shortcuts import render, redirect
from .forms import ScheduleForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from subject.models import Subject
from django.contrib import messages


def create_schedule(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.subject = subject
            schedule.save()
            messages.success(request, 'Schedule created successfully!')
            html = render_to_string('courses/schedule_template.html', {'schedule': schedule})

            return JsonResponse({'status': 'success', 'html': html})
    
    return JsonResponse({'status': 'failed', 'error': 'invalid request'}), 400
