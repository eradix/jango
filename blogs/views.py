from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from .forms import PostForm, PostModelForm
from django.views.decorators.http import require_POST


def index(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts
    }
    return render(request, 'index.html', context)

def show_post(request,id):

    post = get_object_or_404(Post, id=id)

    context = {
        'post' : post
    }

    return render(request, 'show_post.html', context)

def create_post(request):
  
  if request.method == 'POST':
    form = PostForm(request.POST)
    if form.is_valid():
      title = form.cleaned_data['title']
      body = form.cleaned_data['body']
      id = form.cleaned_data['category'].id

      post = Post(title=title, 
                  body=body, 
                  category=Category.objects.get(id=id))
      post.save()

      latest_id = Post.objects.latest('id').id

      return redirect('show_post', latest_id)
  else:
    form = PostForm()
    
  return render(request, 'form_post.html', {'form': form})


#update
def update_post(request,id):

    post = get_object_or_404(Post, id=id)
  
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('show_post', post.id)
    else:
        form = PostModelForm(instance=post)

    return render(request, 'form_post.html', {'form': form})

#delete
@require_POST
def destroy_post(request,id):
  
  post = get_object_or_404(Post, id=id)

  if request.method == 'POST':
    
    post.delete()

    return redirect('index')
