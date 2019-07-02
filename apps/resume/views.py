from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import Http404, HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ResumeItemForm
from .models import ResumeItem, Resume, ResumeItemLink


@login_required
def resume_view(request, resume_pk):
    """
    Handle a request to view a user's resume.
    :param request: http request
    :param resume_pk: Database ID of the Resume to display
    """
    resume_items = ResumeItem.objects \
        .filter(user=request.user) \
        .order_by('-start_date')

    return render(request, 'resume/resume.html', {
        'resume_items': resume_items,
        'resume_pk': resume_pk
    })


@login_required
@transaction.atomic
def resume_item_create_view(request, resume_pk):
    """
    Handle a request to create a new resume item.
    Since we are updating two linked objects, the view is marked atomic
    in order to ensure consistency.

    :param request: http request
    :param resume_pk: Database ID of the Resume we came from.
    """
    if request.method == 'POST':
        resume = get_object_or_404(Resume, pk=resume_pk, user=request.user)

        form = ResumeItemForm(request.POST)
        if form.is_valid():
            new_resume_item = form.save(commit=False)
            new_resume_item.user = request.user
            new_resume_item.save()
            resume_link = ResumeItemLink(resume=resume,
                                         resumeitem=new_resume_item,
                                         order=0)
            resume_link.save()
            return redirect("resume-item-edit", resume.pk, new_resume_item.id)
    else:
        form = ResumeItemForm()

    return render(request, 'resume/resume_item_create.html', {'form': form, 'resume_pk': resume_pk})


@login_required
def resume_item_edit_view(request, resume_pk, resume_item_id):
    """
    Handle a request to edit a resume item.

    :param request: http request
    :param resume_pk: Database ID of Resume we came from.
    :param resume_item_id: The database ID of the ResumeItem to edit.
    """
    try:
        resume_item = ResumeItem.objects \
            .filter(user=request.user) \
            .get(id=resume_item_id)
    except ResumeItem.DoesNotExist:
        raise Http404

    template_dict = {}

    if request.method == 'POST':
        if 'delete' in request.POST:
            resume_item.delete()
            return redirect("resume-view", resume_pk)

        form = ResumeItemForm(request.POST, instance=resume_item)
        if form.is_valid():
            form.save()
            form = ResumeItemForm(instance=resume_item)
            template_dict['message'] = 'Resume item updated'
    else:
        form = ResumeItemForm(instance=resume_item)

    template_dict['form'] = form
    template_dict['resume_pk'] = resume_pk

    return render(request, 'resume/resume_item_edit.html', template_dict)


@method_decorator(login_required, name='dispatch')
class ResumeListView(ListView):
    """
    List of all resumes for a user.
    We order by last-updated by default.
    """

    template_name = "resume/resume_list.html"
    context_object_name = "resumes"

    def get_queryset(self):
        return Resume.objects \
            .filter(user=self.request.user) \
            .order_by("-updated_on")


@method_decorator(login_required, name='dispatch')
class ResumeDetailView(DetailView):
    """
    View resume
    """
    template_name = "resume/resume.html"
    context_object_name = "resume"
    model = Resume

    def get_context_data(self, **kwargs):
        """ add roles to the view """
        context = super(ResumeDetailView, self).get_context_data(**kwargs)
        context['resumelinks'] = context['object'].resumeitemlink_set.order_by('order')
        return context


@method_decorator(login_required, name='dispatch')
class ResumeCreate(CreateView):
    """
    Create resume basic properties.
    """
    model = Resume
    template_name = "resume/resume_create.html"
    context_object_name = "resume"
    fields = ['label', 'description', 'intro']

    def form_valid(self, form):
        """ set the user """
        if not form.is_valid():
            return super(ResumeCreate, self).form_invalid(form)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class ResumeEdit(UpdateView):
    """
    Edit resume basic properties.
    """
    model = Resume
    template_name = "resume/resume_edit.html"
    context_object_name = "resume"
    fields = ['label', 'description', 'intro']

    def form_valid(self, form):
        """ ensure the user matches """
        if not form.is_valid():
            return super(ResumeEdit, self).form_invalid(form)

        edited = form.save(commit=False)
        if edited.user.pk != self.request.user.pk:
            # tbh here we should probably bail to home, but anyway...
            return super(ResumeEdit, self).form_invalid(form)
        else:
            edited.save()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class ResumeDelete(DeleteView):
    """
    Delete resume
    """
    model = Resume
    success_url = reverse_lazy('resume-list')
