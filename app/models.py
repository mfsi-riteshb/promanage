from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class Profile(models.Model):
    Gender = (("Male", "Male"), ("Female", "Female"), ("None", "None"))
    dob = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    activation_key = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=Gender, default="None")
    home_address = models.CharField(max_length=50, default="", null=True)


class Education(models.Model):

    current_year = datetime.now().year
    # create tuple for year like( (1930,1930),.....,(2012,2012)
    YEARS = map(lambda x: (x, x), range(1950, current_year - 4))
    name = models.CharField(max_length=50, blank=False)
    board_university = models.CharField(max_length=100, default="")
    passing_year = models.CharField(max_length=4, choices=YEARS)
    percentage = models.FloatField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Skills(models.Model):

    name = models.CharField(max_length=30)
    profile = models.ManyToManyField(Profile)


class Hobbies(models.Model):

    name = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Project(models.Model):

    name = models.CharField(max_length=200)
    url = models.URLField(max_length=100)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Experience(models.Model):

    company = models.CharField(max_length=200)
    designation = models.CharField(max_length=50)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
