from django.db import models
from django.db.models import CASCADE
from django.urls import reverse


class ResumeItem(models.Model):
    """
    A single resume item, representing a job and title held over a given period
    of time.
    """
    user = models.ForeignKey('auth.User')

    title = models.CharField(max_length=127)
    company = models.CharField(max_length=127)

    start_date = models.DateField()
    # Null end date indicates position is currently held
    end_date = models.DateField(null=True, blank=True)

    description = models.TextField(max_length=2047, blank=True)

    def __unicode__(self):
        return "{}: {} at {} ({})".format(self.user.username,
                                          self.title,
                                          self.company,
                                          self.start_date.isoformat())


class Resume(models.Model):
    """
    A single resume
    """
    user = models.ForeignKey('auth.User')

    # editable properties
    label = models.CharField(max_length=255,
                             default="Awesome Professional",
                             help_text="Resume Title")
    intro = models.TextField(
        help_text="Long-form intro text visible on resume")
    description = models.TextField(
        help_text="Meta description or notes not visible on resume")

    # timestamps
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # convenience wiring
    def get_absolute_url(self):
        return reverse('resume-view', kwargs={'pk': self.pk})

    def __unicode__(self):
        return "{label}".format(
            label=self.label
        )

    def __str__(self):
        return self.__unicode__()


class ResumeItemLink(models.Model):
    """
    Explicit join between resume and jobs so that we can have manual ordering
    and other custom properties eventually.
    """
    resume = models.ForeignKey(Resume, on_delete=CASCADE)
    resumeitem = models.ForeignKey(ResumeItem, on_delete=CASCADE)
    order = models.PositiveSmallIntegerField(default=0, null=False, blank=False)

    def __unicode__(self):
        return "{resume_title} / {order} / {item_title}".format(
            resume_title=self.resume.label,
            order=self.order,
            item_title=self.resumeitem.title
        )

    def __str__(self):
        return self.__unicode__()
