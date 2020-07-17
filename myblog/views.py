from django.shortcuts import render, get_object_or_404,redirect
from .models import Post, Comment,Subscription, Categories
from taggit.models import Tag
from django.contrib.auth.signals import user_logged_out,user_logged_in
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from .forms import SubscribeForm,PostForm, CategoryPost,CommentForm
from django.views.generic import ListView, View,DeleteView
from django.views import View
from django.db.models import Count
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from django.template.loader import render_to_string
# Create your views here.

def category_count():
    queryset = Post\
        .objects \
        .values('category__title')\
        .annotate(Count('category__title'))
    return queryset

def login(request):
    form = UserCreationForm()
    return render(request, 'myblog/login.html', {'form': form})


def contact(request):
    return render(request, 'myblog/contact.html')

def listpost(request):
    form = SubscribeForm()
    queryset = Post.published.all()
    cat = Categories.objects.all()
    cat_count = category_count()
    paginator = Paginator(queryset, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
                'cat': cat,
                'form':form,
                'posts': queryset,
                'page_obj': page_obj,
                
        }

    return render(request, 'myblog/index.html', context)
    


class postList(ListView):
    model = Post
    paginate_by = 2
    context_object_name= "posts"
    template_name = 'myblog/index.html'


    def get_context_data(self, **kwargs):
        latest = Post.objects.order_by('-created')[0:3]
        cat = Categories.objects.all()
        form = SubscribeForm()
        context = super().get_context_data(**kwargs)
        context['cat'] = cat
        context['form'] = form
        context['latest'] = latest
        return context
    
    def get_queryset(self):
        return super(postList, self).get_queryset().filter(post=True)


def search(request):
    queryset = Post.objects.all()
    search = request.GET.get('item')
    cat = Categories.objects.all()
    
    if queryset.filter(title__icontains = search).exists():
        post = queryset.filter(title__icontains = search)
        return render(request, 'myblog/index.html', {'posts': post, 'cat': cat})
    else:
        post = request.GET.get('item')
        return render(request, 'myblog/not_found.html', {'posts': post, 'cat': cat})
        

def mycategory(request, pk):

    Cat = Post.objects.filter(category__title=pk)
    cat = Categories.objects.all()
    return render(request, 'myblog/index.html', {'posts': Cat,'cat': cat,})


# def subscribe(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         sub = Subscription()
#         sub.email = email
#         sub.save()

#         return JsonResponse("")


def subscribe(request):
    form = SubscribeForm()
    # if request.method == 'POST':
    #     form = SubscribeForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('myblog:post')

    if request.is_ajax():
        email = request.POST['email']
        post = Subscription()
        if Subscription.objects.filter(email=email).exists():
            return JsonResponse({
            'msg': 'wrong'
            })
        post.email = email
        post.save()
        return JsonResponse({
            'msg': 'Success'
        })

    return render(request, 'myblog/index.html', {'form': form})

     
        



# class IndexView(View):

#     def get(self, request, *args, **kwargs):


def post_detail(request, year, month, post):
    post = get_object_or_404(Post, slug=post,
                            status='published',
                            publish__year=year,
                            publish__month=month,
                            )
    cat = Categories.objects.all()
    form = CommentForm()
    show = post.tags.similar_objects()
    latest = Post.objects.order_by('-created')[0:3]

    context = {'post': post,
             'cat':cat,
             'form':form,
             'related_post': show,
             'latest': latest,
            }
    if request.is_ajax():
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        parent_obj = None

        
        
        
        try:
            parent_id = int(request.POST['parent_id'])
        except:
            parent_id = None
        
        if parent_id:
            parent_qs = Comment.objects.filter(id= parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()
        
        comment = Comment()
        comment.name = name
        comment.email = email
        comment.message = message
        comment.post = post
        comment.parent = parent_obj
        comment.save()

    
        html = render_to_string('myblog/comment_section.html', context,request=request)
        return JsonResponse({'form':html})

    
    return render(request,
            'myblog/detail.html',context )

def search_titles(request):
    if request.method == 'POST':
        search_text = request.POST['item']
    else:
        search_text = ''

    classes = Post.objects.filter(title__contains=search_text)

    return render_to_response('blog/index.html', {'classes': classes})


def comment(request):
    if request.is_ajax():
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        


        comment = Comment()
        comment.name = name
        comment.email = email
        comment.message = message
        comment.post = post
        comment.save()


        
        html = render_to_string('myblog/comment_section.html', context,request=request)
        return JsonResponse({'form':html})

# admin-------------

def create(request):

    topic = "Update Post"
    if request.method =="POST":
        form = PostForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.info(request, "Message sent")
            return redirect('myblog:create')
    else:
        form = PostForm()
    return render(request, 'myblog/createpost.html', {'form': form})

def createCategory(request):
    if request.method =="POST":
        form = CategoryPost(request.POST or None)
        if form.is_valid():
            form.save()
            messages.info(request, "Category Created")
            return redirect('myblog:create')
    else:
        form = CategoryPost()
    return render(request, 'myblog/create_category.html', {'form': form})

def edit(request, pk=None):
    post = get_object_or_404(Post, pk =pk)
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "re saved")
        except Exception as e:
            form = PostForm()
            messages.warning(request,"Had an error, {}".format(e))
    else:
        form = PostForm(instance=post)

    context = {
        'form':form,

    }

    return render(request,'myblog/createpost.html', context)

def delete(request, pk=None):
   post = get_object_or_404(Post, pk=pk)
   post.delete()
   messages.info(request, "Message delete")
   return redirect("myblog:post")


def show_message(sender, user, request, **kwargs):
    # whatever...
    messages.info(request, 'You have been logged out.')

user_logged_out.connect(show_message)

def show_message1(sender, user, request, **kwargs):
    username = None
    messages.info(request, 'Welcome admin :)')

user_logged_in.connect(show_message1)