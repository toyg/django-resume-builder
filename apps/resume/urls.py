from django.conf.urls import url

from . import views

urlpatterns = [
    # Resume class-based views
    url(r'^$', views.ResumeListView.as_view(),
        name="resume-list"),
    url(r'^create/$', views.ResumeCreate.as_view(),
        name="resume-create"),
    url(r'^(?P<pk>\d+)/edit$', views.ResumeEdit.as_view(),
        name="resume-edit"),
    url(r'^(?P<pk>\d+)/delete$', views.ResumeDelete.as_view(),
        name="resume-delete"),
    url(r'^(?P<pk>\d+)$', views.ResumeDetailView.as_view(),
        name="resume-view"),

    # Item-editing with old-style views
    url(r'^(?P<resume_pk>\d+)/item/edit(?P<resume_item_id>\d+)$',
        views.resume_item_edit_view,
        name='resume-item-edit'),
    url(r'^(?P<resume_pk>\d+)/item/create$',
        views.resume_item_create_view,
        name='resume-item-create')
]
