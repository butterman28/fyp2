from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from djmoney.models.fields import *
from PIL import Image
from django.urls import reverse

questiontype = (
    ("objective", "Objective"),
    ("theory", "Theory"),
)
optype = (
    ("op1", "Op1"),
    ("op2", "Op2"),
    ("op3", "Op3"),
    ("op4", "Op4"),
)


class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    font_size = models.IntegerField(default=16)
    word_spacing = models.IntegerField(default=5)
    color_theme = models.CharField(max_length=10, default="#ffffff")
    font_color = models.CharField(max_length=10, default="#000000")
    brightness = models.IntegerField(default=100)


class Lecturers(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    qualifications = models.CharField(max_length=5000, blank=False, null=False)
    proofofqualific = models.ImageField(
        verbose_name="Proof Of Qualifications",
        default="default.jpg",
        upload_to="qualifications",
    )


class Courses(models.Model):
    name = models.CharField(max_length=5000, blank=False, null=False)
    description = models.CharField(max_length=5000, blank=False, null=False)
    lecturer = models.ForeignKey(Lecturers, on_delete=models.CASCADE)


class courseenrollment(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    tutored = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("course-detail", kwargs={"pk": self.course.pk})


class topics(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    name = models.CharField(max_length=5000, blank=False, null=False)
    description = models.CharField(max_length=5000, blank=False, null=False)
    content = models.TextField()
    video_file = models.FileField(upload_to="videos")

    def get_absolute_url(self):
        return reverse("topic-detail", kwargs={"pk": self.pk})


class subtitles(models.Model):
    topic = models.ForeignKey(topics, on_delete=models.CASCADE)
    subtitle = models.FileField(upload_to="srt_files/")


class topicsquiz(models.Model):
    topic = models.ForeignKey(topics, on_delete=models.CASCADE)
    question = models.CharField(max_length=5000, blank=False, null=False)
    questiontype = models.CharField(
        max_length=5000, choices=questiontype, blank=False, null=False
    )

    def get_absolute_url(self):
        return reverse("topic-detail", kwargs={"pk": self.topic.pk})


class topicobj(models.Model):
    objquestion = models.ForeignKey(topicsquiz, on_delete=models.CASCADE)
    op1 = models.CharField(max_length=5000, blank=False, null=False)
    op2 = models.CharField(max_length=5000, blank=False, null=False)
    op3 = models.CharField(max_length=5000, blank=False, null=False)
    op4 = models.CharField(max_length=5000, blank=False, null=False)
    answer = models.CharField(
        max_length=5000,
        verbose_name="Correct Option/Answer",
        choices=optype,
        blank=False,
        null=False,
    )

    def get_absolute_url(self):
        return reverse("topic-detail", kwargs={"pk": self.objquestion.topic.pk})


class objanssheet(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(topicobj, on_delete=models.CASCADE)
    answerfilled = models.CharField(
        max_length=5000, choices=optype, blank=False, null=False
    )
    status = models.BooleanField(default=False)


class theoryanssheet(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(topicsquiz, on_delete=models.CASCADE)
    answer = models.TextField(null=True)


class Teachers(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    handlesize = models.PositiveIntegerField(
        verbose_name="size of class you can handle", default=3, blank=False, null=False
    )

    def get_absolute_url(self):
        return reverse("teacher-profile", kwargs={"pk": self.pk})


class classroom(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)


class classparticipants(models.Model):
    classroomid = models.ForeignKey(classroom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# Create your models here.
