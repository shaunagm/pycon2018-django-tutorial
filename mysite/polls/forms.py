from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('question', 'created_date', 'author', 'text',)

    def __init__(self, question_pk=None, author=None, *args, **kwargs):
            super(CommentForm, self).__init__(*args, **kwargs)
            if question_pk:
                self.fields['question'].initial = question_pk
                self.fields['question'].widget = forms.HiddenInput()
            if author:
                self.fields['author'].initial = author
                self.fields['author'].widget = forms.HiddenInput()
