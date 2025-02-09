from typing import List
from django.contrib.auth import get_user_model
from django.db import models


class Voting(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    blocked = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    def like(self, user: get_user_model):
        like, created = Like.objects.get_or_create(user=user, voting=self)
        if not created:
            like.active = not like.active
            like.save()

    def is_user_voted(self, user: get_user_model) -> bool:
        return VoteFact.objects.filter(user=user).filter(variant__question__voting=self).exists()

    def publish(self):
        self.published = True
        self.save()

    @staticmethod
    def get_active_votings() -> List:
        return Voting.objects.filter(blocked=False).filter(published=True).all()

    def get_questions(self) -> List:
        return Question.objects.filter(voting=self).all()

    @staticmethod
    def get_votings_of_user(user: get_user_model) -> List:
        return Voting.objects.filter(author=user).all()

    @staticmethod
    def get_voted_votings(user: get_user_model) -> List:
        votings = {
            vote_fact.variant.question.voting for vote_fact in VoteFact.objects.filter(user=user).all()
        }
        return list(votings)

    @staticmethod
    def get_liked_votings(user: get_user_model) -> List:
        return Voting.objects.filter(like__user=user, like__active=True).all()

    def get_likes_count(self) -> int:
        return Like.objects.filter(voting=self, active=True).count()

    def is_user_liked(self, user: get_user_model) -> bool:
        return Like.objects.filter(user=user, voting=self, active=True).exists()


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
    active = models.BooleanField(default=True)


class Complaint(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    text = models.TextField()
    is_active = models.BooleanField(default=True)

    @staticmethod
    def get_opened_complains() -> List:
        return Complaint.objects.filter(is_active=True).all()

    def block(self):
        self.is_active = False
        self.voting.blocked = True
        self.voting.save()
        self.save()

    def skip(self):
        self.is_active = False
        self.save()
