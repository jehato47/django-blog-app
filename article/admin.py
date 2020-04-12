from django.contrib import admin
from .models import Article, Comment
from embed_video.admin import AdminVideoMixin

# Register your models here.


admin.site.register(Comment)


@admin.register(Article)
class ArticleAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ["title", "created_date", "author", "article_image"]
    list_display_links = ["title", "created_date"]
    search_fields = ["title"]
    list_filter = ["title"]

    class Meta:
        model = Article


