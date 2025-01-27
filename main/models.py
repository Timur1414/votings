from typing import List

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


class Voting(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    blocked = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def is_user_voted(self, user: get_user_model) -> bool:
        return VoteFact.objects.filter(user=user).filter(variant__question__voting=self).exists()

    def publish(self):
        self.published = True
        self.save()

    @staticmethod
    def get_active_votings() -> List:
        return Voting.objects.filter(blocked=False).filter(published=True).all().order_by('likes')

    def get_questions(self) -> List:
        return Question.objects.filter(voting=self).all()


class Question(models.Model):
    QUESTION_TYPES = [
        (1, 'Single Choice'),
        (2, 'Multiple Choice'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    type = models.IntegerField(choices=QUESTION_TYPES)

    def get_variants(self) -> List:
        return Variant.objects.filter(question=self).all()


class Variant(models.Model):
    text = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def is_user_voted(self, user: get_user_model) -> bool:
        return VoteFact.objects.filter(user=user).filter(variant=self).exists()

    def calculate_votes(self) -> int:
        count = VoteFact.objects.filter(variant=self).count()
        total_count = VoteFact.objects.filter(variant__question=self.question).count()
        return int(count / total_count * 100) if total_count != 0 else 0


class VoteFact(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)

    @staticmethod
    def vote(user: get_user_model, variant: Variant):
        obj = VoteFact.objects.create(user=user, variant=variant)
        obj.save()


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)


class Complaint(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    text = models.TextField()
    is_active = models.BooleanField(default=True)
