from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title= models.CharField(max_length=30)
    keywords=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10,choices=STATUS)
    slug=models.SlugField(null=False,unique=True)
    parent=TreeForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '->'.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_decription = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})

class Book(models.Model):
    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    title= models.CharField(max_length=100)
    keywords=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    yazar=models.CharField(max_length=50)
    basimyili=models.IntegerField()
    baskisira=models.IntegerField()
    yayinevi=models.CharField(max_length=50)
    stok= models.IntegerField()
    detail=RichTextUploadingField()
    status=models.CharField(max_length=10,choices=STATUS)
    slug=models.SlugField(null=False,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'slug':self.slug})

class Images(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_decription = 'Image'

class Comment(models.Model):
    STATUS=(
        ('New','Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    product=models.ForeignKey(Book,on_delete=models.CASCADE)
    users=models.ForeignKey(User,on_delete=models.CASCADE)
    subject= models.CharField(max_length=50)
    comment=models.TextField(max_length=200,blank=True)
    rate=models.IntegerField(blank=True)
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.subject
class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['subject','comment','rate']