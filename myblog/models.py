from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager



class Categories(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('myblog:filt', kwargs={'pk': self.pk})



class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name='blog_posts')
    body = RichTextUploadingField()
    # body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    post = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                            choices=STATUS_CHOICES,
                            default='published')
    category = models.ForeignKey(Categories, on_delete= models.CASCADE, blank=True, null=True)
    tags = TaggableManager()

    


    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    def get_absolute_url1(self):
        return reverse('myblog:post_detail',
                        args=[self.publish.year,
                            self.publish.month,
                            self.slug]
                            )


    def post_list_by_tag(self):
        return reverse("core:post_list_by_tag", kwargs={
            'tag.slug': self.tag.slug
        })

    def get_absolute_url(self):
        return reverse('myblog:edit',kwargs = {'pk': self.pk})
    
    def get_absolute_url(self):
        return reverse('myblog:delete',kwargs = {'pk': self.pk})
    

    def get_comments(self):
        return self.comments.all().filter(parent=None).order_by('-created')

class Comment(models.Model):

    name = models.CharField(max_length=80)
    email = models.EmailField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    post = models.ForeignKey(Post, on_delete= models.CASCADE, blank=True, null=True, related_name='comments')
    parent = models.ForeignKey('self', on_delete= models.CASCADE, null=True, related_name='replies')
    
    

    
    
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
    
    


class Subscription(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email