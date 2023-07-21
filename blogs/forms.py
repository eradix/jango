from django import forms
from .models import Category, Post

class PostForm(forms.Form):
  
    category = forms.ModelChoiceField(
      label = 'Category', 
      queryset = Category.objects.all(),
      widget=forms.Select(attrs={'class': 'form-control'}))
  
    title = forms.CharField(
      label='Title', 
      max_length=100,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
  
    body = forms.CharField(
      label=' Body', 
      widget= forms.Textarea(attrs={'class': 'form-control'}))

#model form used for update
class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
      
        fields = ['category', 'title', 'body']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }