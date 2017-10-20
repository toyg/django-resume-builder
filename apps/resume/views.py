from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import ResumeItem


@login_required
def resume_view(request):
    """
    Handle a request to view a user's resume.
    """
    resume_items = ResumeItem.objects\
        .filter(user=request.user)\
        .order_by('-start_date')

    return render(request, 'resume/resume.html', {
        'resume_items': resume_items
    })
