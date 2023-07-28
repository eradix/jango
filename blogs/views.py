from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from .forms import PostForm, PostModelForm, SearchPostForm
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

@login_required
def index(request):
    
    search =  request.GET.get('q')

    search_form = SearchPostForm(request.GET)

    if search:
       posts = Post.objects.filter(Q(title__icontains=search) | Q(body__icontains=search))
    else:   
      posts = Post.objects.all()

    context = {
        'posts' : posts,
        'search_form' : search_form,
        'search_q' : search,
        'header' : "Home / Posts"
    }
    return render(request, 'index.html', context)

@login_required
def show_post(request,id):

    post = get_object_or_404(Post, id=id)

    context = {
        'post' : post,
        'header' : "Post / info"
    }

    return render(request, 'show_post.html', context)

@login_required
def create_post(request):
  
  if request.method == 'POST':
    form = PostForm(request.POST)
    if form.is_valid():
      title = form.cleaned_data['title']
      body = form.cleaned_data['body']
      id = form.cleaned_data['category'].id
      user_id = request.user.id

      post = Post(title=title, 
                  body=body, 
                  category=Category.objects.get(id=id),
                  user = User.objects.get(id=user_id)
                  )
      post.save()

      latest_id = Post.objects.latest('id').id

      # create flash message
      messages.success(request, "Post successfully created.")

      return redirect('show_post', latest_id)
  else:
    form = PostForm()
    
  return render(request, 'form_post.html', {'form': form, 'header' : "Post / create"})


#update
@login_required
def update_post(request,id):

    post = get_object_or_404(Post, id=id)

    #check if current user owns this post
    if not request.user.is_superuser and request.user.id != post.user.id:
       messages.error(request, "Unauthorized access.")
       return redirect('show_post', id)
  
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            form.save()

            # create flash message
            messages.success(request, "Post successfully updated.")
            return redirect('show_post', post.id)
    else:
        form = PostModelForm(instance=post)

    return render(request, 'form_post.html', {'form': form, 'header' : "Post / edit"})

#delete
@require_POST
@login_required
def destroy_post(request,id):
  
  #get post
  post = get_object_or_404(Post, id=id)

  #check if current user owns this post
  if not request.user.is_superuser and request.user.id != post.user.id:
    messages.error(request, "Unauthorized access.")
    return redirect('show_post', id)
  
  #delete the post
  post.delete()

  # create flash message
  messages.success(request, "Post successfully deleted.")

  return redirect('index')
