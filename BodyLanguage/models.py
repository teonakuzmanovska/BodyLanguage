from django.contrib.auth.models import User
from django.db import models


class Meaning(models.Model):
    meaning = models.CharField(max_length=50)

    def str(self):
        return str(self.meaning)


class Context(models.Model):
    context = models.CharField(max_length=50)

    def str(self):
        return str(self.context)


class Behaviour(models.Model):
    behaviour = models.CharField(max_length=50)

    def str(self):
        return str(self.behaviour)


class Gesture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gesture = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/", blank=True)
    meaning = models.ManyToManyField(Meaning)  # meaning of gesture
    context = models.ManyToManyField(Context, blank=True)  # optional context
    behaviour = models.ManyToManyField(Behaviour, blank=True)  # optional behaviour
    male = models.BooleanField()
    female = models.BooleanField()
    adult = models.BooleanField()
    child = models.BooleanField()

    def str(self):
        return str(self.meaning)


class Question(models.Model):
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    category = models.CharField(max_length=200, null=True)

    def str(self):
        return str(self.question)


class Results(models.Model):
    category = models.CharField(max_length=200)
    points = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def str(self):
        return str(self.category)
