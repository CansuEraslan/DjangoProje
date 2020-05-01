from django.contrib import admin

# Register your models here.
from book.models import Category, Book, Images


class BookImageInline(admin.TabularInline):
    model = Images
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'yazar', 'yayinevi', 'basimyili', 'stok','image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [BookImageInline]



class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'book', 'image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Images,ImagesAdmin)