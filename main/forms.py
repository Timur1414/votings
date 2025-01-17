from django import forms
from main.models import Voting, Question, Variant


class CreateVotingForm(forms.ModelForm):
    class Meta:
        model = Voting
        fields = ['title', 'author']
        labels = {
            'title': 'Voting Title',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'author': forms.HiddenInput()
        }


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'type', 'voting']
        labels = {
            'title': 'Question Title',
            'description': 'Question Description',
            'type': 'Question Type',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'voting': forms.HiddenInput(),
        }


class CreateVariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['text', 'question']
        labels = {
            'text': 'Variant Text',
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'question': forms.HiddenInput(),
        }
