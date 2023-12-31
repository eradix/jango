from django import forms
from .models import Category, Post

# class form for creating post
# class PostForm(forms.Form):
  
#     category = forms.ModelChoiceField(
#       label = 'Category', 
#       queryset = Category.objects.all(),
#       widget=forms.Select(attrs={'class': 'form-control'}))
  
#     title = forms.CharField(
#       label='Title', 
#       max_length=100,
#       widget=forms.TextInput(attrs={'class': 'form-control'}))
  
#     body = forms.CharField(
#       label=' Body', 
#       widget= forms.Textarea(attrs={'class': 'form-control'}))
    
#     post_image = forms.FileField(
#         label= 'Post image',
#         widget= forms.ClearableFileInput(attrs={'class': 'form-control', 'accept' : 'image/*'}))

#model form used for update
class PostModelForm(forms.ModelForm):

    class Meta:
        model = Post
      
        fields = ['category', 'title', 'body' , 'post_image']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'post_image' : forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
    
  

#search form
class SearchPostForm(forms.Form):
    q = forms.CharField( 
      label='',
      required = False,
      max_length=100,
      widget=forms.TextInput(attrs={'class': 'form-control me-2', 'placeholder' : 'Search post'}))