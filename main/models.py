from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


class Voting(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    blocked = models.BooleanField(default=False)
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])


class Question(models.Model):
    QUESTION_TYPES = [
        (1, 'Single Choice'),
        (2, 'Multiple Choice'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    type = models.IntegerField(choices=QUESTION_TYPES)


class Variant(models.Model):
    text = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class VoteFact(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)


class Complaint(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    text = models.TextField()
    is_active = models.BooleanField(default=True)
