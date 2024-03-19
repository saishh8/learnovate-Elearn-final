from django.db import models
from accounts.models import *

from courses.models import *

# Create your models here.


class LearnerVideo(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Course_Videos, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('learner', 'video')

    def __str__(self):
        return f"{self.learner.email} - {self.video.title}"





class LearnerCourses(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)
    learner = models.ForeignKey(User, on_delete=models.CASCADE)


class LearnerPoints(models.Model):
    learner = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField()
