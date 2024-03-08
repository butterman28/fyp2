from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
gender = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
)
# disabilities = (("blind", "Blind"), ("deaf", "Deaf"), (du))


class samaritanProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    grade = models.CharField(
        max_length=5000,
        help_text="what is your class if your in sec or primary /level for Uni or Poly students, Enter Respectively",
        blank=True,
        null=True,
    )
    occupation = models.CharField(
        max_length=5000,
        help_text="if not in school but currently employed state your craft",
        blank=True,
        null=True,
    )
    age = models.CharField(max_length=5000, blank=False, null=False)
    address = models.CharField(max_length=5000, blank=True, null=True)
    gender = models.CharField(max_length=5000, choices=gender)
    phonenumber = models.CharField(max_length=5000, blank=False, null=False)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class disabilityProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    grade = models.CharField(
        max_length=5000,
        help_text="what is your class if your in sec or primary /level for Uni or Poly students, Enter respctively",
        blank=True,
        null=True,
    )
    state = models.CharField(
        default="Oyo State", max_length=5000, blank=False, null=False
    )
    city = models.CharField(default="Ibadan", max_length=5000, blank=False, null=False)
    age = models.CharField(max_length=5000, blank=False, null=False)
    phonenumber = models.CharField(max_length=5000, blank=False, null=False)
    gender = models.CharField(max_length=5000, choices=gender)
    disabilities = models.CharField(max_length=5000)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
