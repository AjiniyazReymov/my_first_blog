from django.contrib import admin

from posts.models import Post, PostReview, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    actions = ['approve_posts', 'reject_posts']

    def approve_posts(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected posts have been approved")
    approve_posts.short_description = "Approve selected posts"

    def reject_posts(self, request, queryset):
        queryset.update(status='reject')
        self.message_user(request, "Selected posts have been rejected")
    reject_posts.short_description = "Dismiss selected posts"

class PostReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'stars_given', 'comment']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(PostReview, PostReviewAdmin)
admin.site.register(Category, CategoryAdmin)