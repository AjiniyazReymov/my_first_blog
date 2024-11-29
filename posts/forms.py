from django import forms

from .models import PostReview, Post


class PostCreateForm(forms.ModelForm):
    photo = forms.ImageField(required=False)
    class Meta:
        model = Post
        fields = ['title', 'description', 'photo', 'category']

class PostReviewForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = PostReview
        fields = ['stars_given', 'comment']