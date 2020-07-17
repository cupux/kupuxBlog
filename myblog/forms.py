from django import forms
from .models import Subscription, Post, Categories,Comment

class SubscribeForm(forms.ModelForm):

    class Meta:
        model = Subscription
        fields = '__all__'


        # widget = {
        #     'email': forms.EmailField()
        # }


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'

class CategoryPost(forms.ModelForm):

    class Meta:
        model = Categories
        fields = '__all__'
    
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name','email','message')