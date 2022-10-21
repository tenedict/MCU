from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['title', 'movie_name', 'content', 'grade', 'image', 'thumbnail',]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "리뷰 제목은 30자 이내로 작성해주세요.",
                    "style": "height: 2.5rem; resize: none;",
                }
            ),
            "movie_name": forms.Textarea(
                attrs={
                    "placeholder": "영화 제목은 30자 이내로 작성해주세요.",
                    "style": "height: 2.5rem; resize: none;",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "",
                    "style": "height: 15rem; resize: none;",
                }
            ),
        }
        labels = {
            "title": "리뷰 제목",
            "movie_name": "영화 제목",
            "content": "내용",
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "placeholder": "",
                    "style": "height: 100px; resize: none; width: 100%;",
                }
            ),
        }
        labels = {
            "content": "댓글",
        }