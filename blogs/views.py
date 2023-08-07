from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from .forms import PostModelForm, SearchPostForm
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.core.files.storage import FileSystemStorage
import hashlib
from PIL import Image


@login_required
def index(request):
    
    search =  request.GET.get('q')

    search_form = SearchPostForm(request.GET)

    if search:
       posts = Post.objects.filter(Q(title__icontains=search) | Q(body__icontains=search))
    else:   
      posts = Post.objects.all()

    #pagination
    items_per_page = 10

    paginator = Paginator(posts, items_per_page)
    page_number = request.GET.get('page') if 'page' in request.GET else 1

    #form page links if has search
    page_link = f"?q={search}&page=" if search is not None else "?page="
    
    try:
      posts = paginator.page(page_number)
    except EmptyPage:
      posts = None

    context = {
        'posts' : posts,
        'search_form' : search_form,
        'search_q' : search,
        'page_link' : page_link,
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
    form = PostModelForm(request.POST, request.FILES)
    if form.is_valid():

      form.instance.user = request.user

      post_image = request.FILES.get('post_image', None)

      if post_image:

        # Calculate the hash of the uploaded file's content
        file_hash = hashlib.md5(post_image.read()).hexdigest()

        # Get the file extension
        file_extension = post_image.name.split('.')[-1]

        # Combine the hash and extension to create a unique filename
        form.instance.post_image.name = f"{file_hash}.{file_extension}"
      
      #create post
      post = form.save()

      #if has post_image resize
      if post.post_image:
        image = Image.open(post.post_image.path)
        resized_image = image.resize((640, 960))
        resized_image.save(post.post_image.path)

      #get the id of the created post
      latest_id = Post.objects.latest('id').id

      # create flash message
      messages.success(request, "Post successfully created.")

      #redirect to show_post
      return redirect('show_post', latest_id)
  else:
    form = PostModelForm()
    
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
        form = PostModelForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post_image = request.FILES.get('post_image', None)
            if post_image:
              # Calculate the hash of the uploaded file's content
              file_hash = hashlib.md5(post_image.read()).hexdigest()

              # Get the file extension
              file_extension = post_image.name.split('.')[-1]

              # Combine the hash and extension to create a unique filename
              unique_filename = f"{file_hash}.{file_extension}"

              form.instance.post_image.name = unique_filename
            
            #save the form data
            post = form.save()

            # Resize the uploaded image to 640x960
            if post.post_image:
                image = Image.open(post.post_image.path)
                resized_image = image.resize((640, 960))
                resized_image.save(post.post_image.path)

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
